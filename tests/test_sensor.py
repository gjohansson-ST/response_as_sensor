"""Tests for the Response as Sensor sensor."""

from datetime import timedelta
from typing import Any

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from homeassistant.const import STATE_UNAVAILABLE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .conftest import ACTION, SENSOR_ENTITY_ID


async def _async_next_update(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, interval: timedelta
) -> None:
    """Move the time forward to the next update."""
    freezer.tick(interval)
    async_fire_time_changed(hass)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("loaded_entry")
async def test_sensor_updates(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, response: dict[str, Any]
) -> None:
    """Test the sensor runs the action again after the default frequency."""
    assert hass.states.get(SENSOR_ENTITY_ID).state == "21.5"

    response["value"] = 22
    await _async_next_update(hass, freezer, timedelta(minutes=4))
    assert hass.states.get(SENSOR_ENTITY_ID).state == "21.5"

    await _async_next_update(hass, freezer, timedelta(minutes=1))
    assert hass.states.get(SENSOR_ENTITY_ID).state == "22"


@pytest.mark.usefixtures("loaded_entry")
@pytest.mark.parametrize(
    "options",
    [
        {
            "name": "Temperature",
            "action": ACTION,
            "value_template": "{{ response.value }}",
            "frequency": {"hours": 0, "minutes": 0, "seconds": 30},
        }
    ],
)
async def test_sensor_frequency(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, response: dict[str, Any]
) -> None:
    """Test the sensor runs the action again after the set frequency."""
    response["value"] = 22
    await _async_next_update(hass, freezer, timedelta(seconds=30))

    assert hass.states.get(SENSOR_ENTITY_ID).state == "22"


@pytest.mark.usefixtures("loaded_entry")
@pytest.mark.parametrize(
    ("options", "failing_response"),
    [
        pytest.param(
            {
                "name": "Temperature",
                "action": ACTION,
                "value_template": "{{ response.value }}",
            },
            {"value": 0, "fail": True},
            id="action_error",
        ),
        pytest.param(
            {
                "name": "Temperature",
                "action": ACTION,
                "value_template": "{{ 1 / response.value }}",
            },
            {"value": 0},
            id="template_error",
        ),
    ],
)
async def test_sensor_unavailable(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    response: dict[str, Any],
    failing_response: dict[str, Any],
) -> None:
    """Test the sensor is unavailable when the action or template fails."""
    response["value"] = 2
    await _async_next_update(hass, freezer, timedelta(minutes=5))
    assert hass.states.get(SENSOR_ENTITY_ID).state != STATE_UNAVAILABLE

    response.update(failing_response)
    await _async_next_update(hass, freezer, timedelta(minutes=5))
    assert hass.states.get(SENSOR_ENTITY_ID).state == STATE_UNAVAILABLE

    response.clear()
    response["value"] = 4
    await _async_next_update(hass, freezer, timedelta(minutes=5))
    assert hass.states.get(SENSOR_ENTITY_ID).state != STATE_UNAVAILABLE


@pytest.mark.usefixtures("loaded_entry")
@pytest.mark.parametrize(
    "options",
    [
        {
            "name": "Temperature",
            "action": ACTION,
            "value_template": "{{ response.value }}",
            "icon": "mdi:thermometer",
            "device_class": "temperature",
            "state_class": "measurement",
            "unit_of_measurement": "°C",
            "entity_category": "diagnostic",
        }
    ],
)
async def test_sensor_options(
    hass: HomeAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Test the options are set on the sensor."""
    state = hass.states.get(SENSOR_ENTITY_ID)
    assert state.state == "21.5"
    assert state.attributes["icon"] == "mdi:thermometer"
    assert state.attributes["device_class"] == "temperature"
    assert state.attributes["state_class"] == "measurement"
    assert state.attributes["unit_of_measurement"] == "°C"
    assert (
        entity_registry.async_get(SENSOR_ENTITY_ID).entity_category
        is EntityCategory.DIAGNOSTIC
    )
