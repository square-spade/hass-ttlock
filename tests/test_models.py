from datetime import datetime, timedelta

import pytest

try:
    from pydantic.v1 import BaseModel
except ImportError:
    from pydantic import BaseModel

from custom_components.ttlock.models import (
    EpochMs,
    Features,
    Lock,
    OnOff,
    PassageModeConfig,
    Passcode,
)


class TestEpochMs:
    class model_under_test(BaseModel):
        ts: EpochMs

    @pytest.mark.parametrize(
        ("epoch", "tz", "day", "hour"),
        [
            [1675400802000, "Europe/Amsterdam", 5, 6],
            [1675400802000, "Pacific/Auckland", 5, 18],
            [1675400802000, "America/Los_Angeles", 4, 21],
            [1682244497000, "Europe/Amsterdam", 7, 12],
            [1682244497000, "Pacific/Auckland", 7, 22],
            [1682244497000, "America/Los_Angeles", 7, 3],
        ],
    )
    async def test_with_tz(self, hass, epoch, tz, day, hour):
        await hass.config.async_set_time_zone(tz)
        ts = self.model_under_test(ts=epoch).ts
        assert ts.isoweekday() == day
        assert ts.hour == hour


class TestPassageModeConfig:
    def test_passage_mode(self):
        parsed = PassageModeConfig.parse_obj(
            {
                "autoUnlock": 2,
                "isAllDay": 2,
                "endDate": 1200,
                "weekDays": [1, 2, 3, 4, 5, 6, 7],
                "passageMode": 1,
                "startDate": 420,
            }
        )
        assert parsed.enabled
        assert not parsed.all_day
        assert not parsed.auto_unlock

    def test_null_start_end_date(self):
        parsed = PassageModeConfig.parse_obj(
            {
                "autoUnlock": 2,
                "isAllDay": 1,
                "endDate": None,
                "weekDays": [1, 2, 3, 4, 5, 6, 7],
                "passageMode": 2,
                "startDate": None,
            }
        )
        assert parsed.start_minute == 0
        assert parsed.end_minute == 0


class TestFeatures:
    @pytest.fixture()
    def features(self, feature_value):
        return Features.from_feature_value(feature_value)

    @pytest.mark.parametrize(
        ["feature_value", "expected"],
        (
            [
                "10C2F44754CF5F7",
                (
                    Features.lock_remotely,
                    Features.unlock_via_gateway,
                    Features.passage_mode,
                    Features.wifi,
                    Features.door_sensor,
                ),
            ],
            [
                "F44354CD5F3",
                (
                    Features.lock_remotely,
                    Features.unlock_via_gateway,
                    Features.passage_mode,
                ),
            ],
        ),
    )
    def test_flags(self, features: Features, expected):
        for feature in Features:
            assert (feature in features) == (feature in expected)


class TestPasscode:
    def test_permanent_code(self):
        code = Passcode.parse_obj(
            {
                "endDate": 0,
                "sendDate": 1690412306000,
                "keyboardPwdId": 311183184,
                "nickName": "Person A",
                "keyboardPwdType": 2,
                "lockId": 4567,
                "keyboardPwdVersion": 4,
                "isCustom": 0,
                "keyboardPwdName": "Person A",
                "keyboardPwd": "1234",
                "startDate": 1690408800000,
                "senderUsername": "some@email.com",
                "receiverUsername": "",
                "status": 1,
            }
        )
        assert code.expired is False

    @pytest.mark.parametrize(
        ("offset", "expired"),
        [
            (timedelta(weeks=-1), True),
            (timedelta(weeks=1), False),
        ],
    )
    def test_temporary_code(self, offset, expired):
        code = Passcode.parse_obj(
            {
                "startDate": 1690408800000,
                "endDate": round((datetime.now() + offset).timestamp() * 1000),
                "keyboardPwdId": 311183184,
                "keyboardPwdType": 3,
                "keyboardPwdName": "Person A",
                "keyboardPwd": "1234",
            }
        )
        assert code.expired == expired


# All the required fields
MINIMAL_LOCK = {
    "lockId": 1,
    "lockName": "A Lock",
    "lockAlias": "My Lock",
    "lockMac": "00:00:00:00:00:0",
    "date": 0,
    "adminPwd": "1234",
}


class TestLock:
    def test_basic_lock(self):
        lock = Lock.parse_obj(
            {
                **MINIMAL_LOCK,
                "lockId": 123,
            }
        )
        assert lock.id == 123

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, OnOff.on),
            (2, OnOff.off),
        ],
    )
    def test_lock_sound(self, value, expected):
        lock = Lock.parse_obj(
            {
                **MINIMAL_LOCK,
                "lockSound": value,
            }
        )
        assert lock.lockSound == expected
