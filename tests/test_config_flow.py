"""Tests for the Response as Sensor config flow."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.response_as_sensor.const import DOMAIN
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from .conftest import ACTION, SENSOR_ENTITY_ID


async def test_user_flow(hass: HomeAssistant) -> None:
    """Test creating a helper through the config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "Temperature",
            "action": ACTION,
            "value_template": "{{ response.value }}",
            "device_class": "temperature",
            "unit_of_measurement": "°C",
            "frequency": {"hours": 0, "minutes": 10, "seconds": 0},
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Temperature"
    assert result["options"] == {
        "name": "Temperature",
        "action": ACTION,
        "value_template": "{{ response.value }}",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "frequency": {"hours": 0, "minutes": 10, "seconds": 0},
    }
    assert hass.states.get(SENSOR_ENTITY_ID).state == "21.5"


async def test_options_flow(hass: HomeAssistant, loaded_entry: MockConfigEntry) -> None:
    """Test changing the options reloads the sensor with the new options."""
    result = await hass.config_entries.options.async_init(loaded_entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"value_template": "{{ response.value * 2 }}", "unit_of_measurement": "°C"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert loaded_entry.options == {
        "name": "Temperature",
        "action": ACTION,
        "value_template": "{{ response.value * 2 }}",
        "unit_of_measurement": "°C",
    }
    state = hass.states.get(SENSOR_ENTITY_ID)
    assert state.state == "43.0"
    assert state.attributes["unit_of_measurement"] == "°C"
