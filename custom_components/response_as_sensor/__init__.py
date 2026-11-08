"""The Response as Sensor component."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_VALUE_TEMPLATE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError, TemplateError
from homeassistant.helpers.template import Template

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up Attribute as sensor from a config entry."""

    if value_template := entry.options.get(CONF_VALUE_TEMPLATE):
        value_template = Template(value_template, hass)
        try:
            value_template.ensure_valid()
        except TemplateError as ex:
            raise ConfigEntryError from ex

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
