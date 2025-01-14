from homeassistant.core import HomeAssistant


async def test_lock_states(hass: HomeAssistant, mock_api_responses, component_setup):
    """Test different lock states."""
    mock_api_responses("default")
    coordinator = await component_setup()
    assert not coordinator.data.locked
