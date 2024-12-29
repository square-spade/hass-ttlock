from homeassistant.core import HomeAssistant


async def test_lock_states(hass: HomeAssistant, mock_api_responses, component_setup):
    """Test different lock states."""
    mock_api_responses("default")
    coordinator = await component_setup()
    assert not coordinator.data.locked


async def test_sensor_states(hass: HomeAssistant, mock_api_responses, component_setup):
    """Test different sensor states."""
    mock_api_responses("sensor")
    coordinator = await component_setup()
    assert not coordinator.data.opened
    assert coordinator.data.locked
