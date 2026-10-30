"""Tests for setting up Response as Sensor."""

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from .conftest import ACTION, SENSOR_ENTITY_ID


async def test_setup_and_unload(
    hass: HomeAssistant, loaded_entry: MockConfigEntry
) -> None:
    """Test setting up and unloading a config entry."""
    assert loaded_entry.state is ConfigEntryState.LOADED
    assert hass.states.get(SENSOR_ENTITY_ID).state == "21.5"

    assert await hass.config_entries.async_unload(loaded_entry.entry_id)
    await hass.async_block_till_done()

    assert loaded_entry.state is ConfigEntryState.NOT_LOADED


@pytest.mark.parametrize(
    "options",
    [
        {
            "name": "Temperature",
            "action": ACTION,
            "value_template": "{{ response.value ",
        }
    ],
)
async def test_invalid_template(
    hass: HomeAssistant, loaded_entry: MockConfigEntry
) -> None:
    """Test an invalid value template fails the setup."""
    assert loaded_entry.state is ConfigEntryState.SETUP_ERROR
    assert hass.states.get(SENSOR_ENTITY_ID) is None
