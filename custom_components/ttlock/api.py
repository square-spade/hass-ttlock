"""API for TTLock bound to Home Assistant OAuth."""
import asyncio
from hashlib import md5
import logging
from secrets import token_hex
import time
from typing import Any, cast
from urllib.parse import urljoin

from aiohttp import ClientSession

from homeassistant.components.application_credentials import AuthImplementation
from homeassistant.helpers import config_entry_oauth2_flow

from .models import Features, Lock, LockState, PassageModeConfig, AutoLockConfig

_LOGGER = logging.getLogger(__name__)
GW_LOCK = asyncio.Lock()


class RequestFailed(Exception):
    """Exception when TTLock API returns an error."""

    pass


class TTLockAuthImplementation(
    AuthImplementation,
):
    """TTLock Local OAuth2 implementation."""

    async def login(self, username: str, password: str) -> dict:
        """Make a token request."""
        return await self._token_request(
            {
                "username": username,
                "password": md5(password.encode("utf-8")).hexdigest(),
            }
        )

    async def async_resolve_external_data(self, external_data: Any) -> dict:
        """Resolve the authorization code to tokens."""
        return dict(external_data)


class TTLockApi:
    """Provide TTLock authentication tied to an OAuth2 based config entry."""

    BASE = "https://euapi.ttlock.com/v3/"

    def __init__(
        self,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize TTLock auth."""
        self._web_session = websession
        self._oauth_session = oauth_session

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self._oauth_session.valid_token:
            await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token["access_token"]

    def _add_auth(self, **kwargs) -> dict:
        kwargs["clientId"] = self._oauth_session.implementation.client_id
        kwargs["accessToken"] = self._oauth_session.token["access_token"]
        kwargs["date"] = str(round(time.time() * 1000))
        return kwargs

    async def get(self, path: str, **kwargs: Any):
        """Make GET request to the API with kwargs as query params."""
        id = token_hex(2)

        url = urljoin(self.BASE, path)
        _LOGGER.debug("[%s] Sending request to %s with args=%s", id, url, kwargs)
        resp = await self._web_session.get(
            url,
            params=self._add_auth(**kwargs),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if resp.status >= 400:
            body = await resp.text()
            _LOGGER.debug(
                "[%s] Request failed: status=%s, body=%s", id, resp.status, body
            )
        else:
            body = await resp.json()
            _LOGGER.debug(
                "[%s] Received response: status=%s: body=%s", id, resp.status, body
            )

        resp.raise_for_status()

        res = cast(dict, await resp.json())
        if res.get("errcode", 0) != 0:
            _LOGGER.debug("[%s] API returned: %s", id, res)
            raise RequestFailed(f"API returned: {res}")

        return cast(dict, await resp.json())

    async def get_locks(self) -> list[int]:
        """Enumerate all locks in the account."""
        res = await self.get("lock/list", pageNo=1, pageSize=1000)
        return [lock["lockId"] for lock in res["list"]]

    async def get_lock(self, lock_id: int) -> Lock:
        """Get a lock by ID."""
        res = await self.get("lock/detail", lockId=lock_id)
        return Lock.parse_obj(res)

    async def get_lock_state(self, lock_id: int) -> LockState:
        """Get the state of a lock."""
        async with GW_LOCK:
            res = await self.get("lock/queryOpenState", lockId=lock_id)
        return LockState.parse_obj(res)

    async def get_lock_passage_mode_config(self, lock_id: int) -> PassageModeConfig:
        """Get the passage mode configuration of a lock."""
        res = await self.get("lock/getPassageModeConfig", lockId=lock_id)
        return PassageModeConfig.parse_obj(res)

    async def set_lock_autolock_config(self, lock_id: int, config: AutoLockConfig) -> bool:
        """ Set the autolock configuration of the lock"""

        async with GW_LOCK:
            res = await self.post(
                "lock/setAutoLockTime",
                lockId=lock_id,
                type=2,  # via gateway
                seconds=10 if config.autolock else -1
            )

        if "errcode" in res and res["errcode"] != 0:
            _LOGGER.error("Failed to unlock %s: %s", lock_id, res["errmsg"])
            return False

        return True

    async def lock(self, lock_id: int) -> bool:
        """Try to lock the lock."""
        async with GW_LOCK:
            res = await self.get("lock/lock", lockId=lock_id)

        if "errcode" in res and res["errcode"] != 0:
            _LOGGER.error("Failed to lock %s: %s", lock_id, res["errmsg"])
            return False

        return True

    async def unlock(self, lock_id: int) -> bool:
        """Try to unlock the lock."""
        async with GW_LOCK:
            res = await self.get("lock/unlock", lockId=lock_id)

        if "errcode" in res and res["errcode"] != 0:
            _LOGGER.error("Failed to unlock %s: %s", lock_id, res["errmsg"])
            return False

        return True

    async def set_passage_mode(self, lock_id: int, config: PassageModeConfig) -> bool:
        """Configure passage mode."""

        async with GW_LOCK:
            res = await self.post(
                "lock/configPassageMode",
                lockId=lock_id,
                type=2,  # via gateway
                passageMode=1 if config.enabled else 2,
                autoUnlock=1 if config.auto_unlock else 2,
                isAllDay=1 if config.all_day else 2,
                startDate=config.start_minute,
                endDate=config.end_minute,
                weekDays=json.dumps(config.week_days),
            )

        if "errcode" in res and res["errcode"] != 0:
            _LOGGER.error("Failed to unlock %s: %s", lock_id, res["errmsg"])
            return False

        return True
