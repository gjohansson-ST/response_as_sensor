"""Fixtures for Response as Sensor tests."""

from typing import Any

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.response_as_sensor.const import DOMAIN
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import HomeAssistantError

SENSOR_ENTITY_ID = "sensor.temperature"
ACTION = [{"action": "test.get_data", "response_variable": "response"}]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations in all tests."""


@pytest.fixture
def response() -> dict[str, Any]:
    """Return the response of the test action, change it to change the response."""
    return {"value": 21.5}


@pytest.fixture(autouse=True)
def register_action(hass: HomeAssistant, response: dict[str, Any]) -> None:
    """Register an action which returns the response."""

    async def get_data(call: ServiceCall) -> dict[str, Any]:
        if response.get("fail"):
            raise HomeAssistantError("Failed to get data")
        return dict(response)

    hass.services.async_register(
        "test", "get_data", get_data, supports_response=SupportsResponse.ONLY
    )


@pytest.fixture
def options() -> dict[str, Any]:
    """Return the options of the config entry."""
    return {
        "name": "Temperature",
        "action": ACTION,
        "value_template": "{{ response.value }}",
    }


@pytest.fixture
def config_entry(options: dict[str, Any]) -> MockConfigEntry:
    """Return a config entry."""
    return MockConfigEntry(domain=DOMAIN, title=options["name"], options=options)


@pytest.fixture
async def loaded_entry(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the integration."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
