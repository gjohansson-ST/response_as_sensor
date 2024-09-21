[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge&cacheSeconds=3600)](https://github.com/hacs/integration)
[![size_badge](https://img.shields.io/github/repo-size/gjohansson-ST/response_as_sensor?style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_sensor)
[![version_badge](https://img.shields.io/github/v/release/gjohansson-ST/response_as_sensor?label=Latest%20release&style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_sensor/releases/latest)
[![download_badge](https://img.shields.io/github/downloads/gjohansson-ST/response_as_sensor/total?style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_sensor/releases/latest)


# Home Assistant create an action call response as it's own sensor
---
**Title:** "Response as sensor"

**Description:** "Create an entity from a service call response data."

**Date created:** 2024-09-21

**Last update:** 2024-09-21

**Join the Discussion on Development:** [https://discord.gg/hP5n4GaPg3](https://discord.gg/hP5n4GaPg3)

---

## Configuration Options

### Set once

- Name: Name of the new entity.
- Action: Which service to call.

### Options that you can change at any time

- Value template: Use a template to construct the final state of the sensor.
- Icon: Icon to use in frontend.
- Device class: Device class (select from list).
- State class: State class (select from list).
- Unit of measurement: UoM to use in frontend (select from list, only temperature, or write your own).
- Frequency: Frequency of the action call, don't set too low.

## Installation

### Option 1 (preferred)

Use [HACS](https://hacs.xyz/) to install
Add as [custom repository](https://hacs.xyz/docs/faq/custom_repositories) to HACS

### Option 2

1. Below config-folder create a new folder called`custom_components` if not already exist.
2. Below new `custom_components` folder create a new folder called `response_as_entity`
3. Upload the files/folders in `custom_components/response_as_sensor` directory to the newly created folder.
4. Restart before proceeding

## Activate integration in HA

[![Add integrations](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=response_as_sensor)

After installation go to "Devices & services" and then "helper" page in HA, press "+ Create helper" and find "Response as sensor"
Follow on-screen information for the required information
No restart needed
