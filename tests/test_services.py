from datetime import timedelta
from unittest.mock import call, patch

import pytest

from custom_components.ttlock.const import (
    DOMAIN,
    SVC_CLEANUP_PASSCODES,
    SVC_CREATE_PASSCODE,
    SVC_LIST_PASSCODES,
)
from custom_components.ttlock.models import AddPasscodeConfig, Passcode, PasscodeType
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.util import dt


class Test_list_passcodes:
    async def test_list_passcodes(
        self, hass: HomeAssistant, component_setup, mock_api_responses
    ):
        """Test list_passcodes service."""
        mock_api_responses("default")
        coordinator = await component_setup()

        passcode = Passcode(
            keyboardPwdId=123,
            keyboardPwdType=PasscodeType.temporary,
            keyboardPwdName="Test Code",
            keyboardPwd="123456",
            startDate=1704067200000,  # 2024-01-01
            endDate=1735689600000,  # 2024-12-31
        )

        with patch(
            "custom_components.ttlock.api.TTLockApi.list_passcodes",
            return_value=[passcode],
        ) as mock:
            response = await hass.services.async_call(
                DOMAIN,
                SVC_LIST_PASSCODES,
                {ATTR_ENTITY_ID: coordinator.entities[0].entity_id},
                blocking=True,
                return_response=True,
            )
            await hass.async_block_till_done()
            assert mock.called

        assert response == {
            "passcodes": {
                coordinator.data.name: [
                    {
                        "name": "Test Code",
                        "passcode": "123456",
                        "type": "temporary",
                        "start_date": "2024-01-01T00:00:00+00:00",
                        "end_date": "2024-12-31T00:00:00+00:00",
                        "expired": False,
                    }
                ]
            }
        }

    async def test_list_passcodes_no_results(
        self, hass: HomeAssistant, component_setup, mock_api_responses
    ):
        """Test list_passcodes service with no passcodes."""
        mock_api_responses("default")
        coordinator = await component_setup()

        with patch(
            "custom_components.ttlock.api.TTLockApi.list_passcodes",
            return_value=[],
        ) as mock:
            response = await hass.services.async_call(
                DOMAIN,
                SVC_LIST_PASSCODES,
                {ATTR_ENTITY_ID: coordinator.entities[0].entity_id},
                blocking=True,
                return_response=True,
            )
            await hass.async_block_till_done()
            assert mock.called

        assert response == {"passcodes": {coordinator.data.name: []}}


class Test_create_passcode:
    async def test_can_create_passcode(
        self, hass: HomeAssistant, component_setup, mock_api_responses
    ):
        mock_api_responses("default")
        coordinator = await component_setup()

        attrs = {
            "passcode_name": "Test User",
            "passcode": 1234,
            "start_time": dt.now() - timedelta(days=1),
            "end_time": dt.now() + timedelta(weeks=2),
        }
        with patch(
            "custom_components.ttlock.api.TTLockApi.add_passcode", return_value=True
        ) as mock:
            await hass.services.async_call(
                DOMAIN,
                SVC_CREATE_PASSCODE,
                {
                    ATTR_ENTITY_ID: coordinator.entities[0].entity_id,
                    **attrs,
                },
            )
            await hass.async_block_till_done()
            assert mock.call_args_list == [
                call(
                    coordinator.lock_id,
                    AddPasscodeConfig(
                        passcode=attrs["passcode"],
                        passcodeName=attrs["passcode_name"],
                        startDate=attrs["start_time"].timestamp() * 1000,
                        endDate=attrs["end_time"].timestamp() * 1000,
                    ),
                )
            ]


class Test_cleanup_passcodes:
    @pytest.mark.parametrize("return_response", (True, False))
    async def test_works_when_there_is_nothing_to_do(
        self, hass: HomeAssistant, component_setup, mock_api_responses, return_response
    ) -> None:
        """Test get schedule service."""
        mock_api_responses("default")
        coordinator = await component_setup()

        with patch(
            "custom_components.ttlock.api.TTLockApi.list_passcodes", return_value=[]
        ) as mock:
            response = await hass.services.async_call(
                DOMAIN,
                SVC_CLEANUP_PASSCODES,
                {ATTR_ENTITY_ID: coordinator.entities[0].entity_id},
                blocking=True,
                return_response=return_response,
            )
            await hass.async_block_till_done()
            assert mock.called

        if return_response:
            assert response == {"removed": []}
        else:
            assert response is None

    async def test_works_when_there_is_an_expired_passcode(
        self,
        hass: HomeAssistant,
        component_setup,
        mock_api_responses,
    ) -> None:
        """Test get schedule service."""
        mock_api_responses("default")
        coordinator = await component_setup()

        with patch(
            "custom_components.ttlock.api.TTLockApi.list_passcodes",
            return_value=[
                Passcode(
                    keyboardPwdId=123,
                    keyboardPwdType=PasscodeType.temporary,
                    keyboardPwdName="Test",
                    endDate=0,
                )
            ],
        ), patch(
            "custom_components.ttlock.api.TTLockApi.delete_passcode", return_value=True
        ) as mock:
            response = await hass.services.async_call(
                DOMAIN,
                SVC_CLEANUP_PASSCODES,
                {ATTR_ENTITY_ID: coordinator.entities[0].entity_id},
                blocking=True,
                return_response=True,
            )
            await hass.async_block_till_done()
            assert mock.call_args_list == [call(coordinator.lock_id, 123)]

        assert response == {"removed": ["Test"]}