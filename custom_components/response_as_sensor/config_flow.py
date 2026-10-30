"""Config flow for Response as Sensor integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import probatio

from homeassistant.components.sensor import CONF_STATE_CLASS
from homeassistant.const import (
    CONF_ACTION,
    CONF_DEVICE_CLASS,
    CONF_ENTITY_CATEGORY,
    CONF_ICON,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE,
    EntityCategory,
    Platform,
)
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)

from .const import CONF_FREQUENCY, DOMAIN

CONFIG_SCHEMA = probatio.Schema(
    {
        probatio.Required(CONF_NAME): selector.TextSelector(),
        probatio.Required(CONF_ACTION): selector.ActionSelector(),
    }
)

OPTIONS_SCHEMA = probatio.Schema(
    {
        probatio.Required(CONF_VALUE_TEMPLATE): selector.TemplateSelector(),
        probatio.Optional(CONF_ICON): selector.IconSelector(),
        probatio.Optional(CONF_DEVICE_CLASS): selector.DeviceClassSelector(
            selector.DeviceClassSelectorConfig(domain=Platform.SENSOR)
        ),
        probatio.Optional(CONF_STATE_CLASS): selector.StateClassSelector(),
        probatio.Optional(CONF_UNIT_OF_MEASUREMENT): selector.UnitOfMeasurementSelector(
            selector.UnitOfMeasurementSelectorConfig(
                context={
                    "filter_device_class": CONF_DEVICE_CLASS,
                    "filter_state_class": CONF_STATE_CLASS,
                }
            )
        ),
        # Sensors can't use the config category
        probatio.Optional(CONF_ENTITY_CATEGORY): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[EntityCategory.DIAGNOSTIC],
                mode=selector.SelectSelectorMode.DROPDOWN,
                translation_key="entity_category",
            )
        ),
        probatio.Optional(CONF_FREQUENCY): selector.DurationSelector(
            selector.DurationSelectorConfig(
                enable_day=False, enable_millisecond=False, allow_negative=False
            )
        ),
    }
)


CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA.extend(OPTIONS_SCHEMA.schema)),
}
OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(OPTIONS_SCHEMA)
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for Response as sensor."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return cast(str, options["name"]) if "name" in options else ""
