[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge&cacheSeconds=3600)](https://github.com/hacs/integration)
[![size_badge](https://img.shields.io/github/repo-size/gjohansson-ST/response_as_entity?style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_entity)
[![version_badge](https://img.shields.io/github/v/release/gjohansson-ST/response_as_entity?label=Latest%20release&style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_entity/releases/latest)
[![download_badge](https://img.shields.io/github/downloads/gjohansson-ST/response_as_entity/total?style=for-the-badge&cacheSeconds=3600)](https://github.com/gjohansson-ST/response_as_entity/releases/latest)


# Home Assistant create an service call response as it's own entity
---
**Title:** "Response as entity"

**Description:** "Create an entity from a service call response data."

**Date created:** 2024-06-25

**Last update:** 2024-06-25

**Join the Discussion on Development:** [https://discord.gg/qyBhBArwHN](https://discord.gg/qyBhBArwHN)

---

## Configuration Options

### Set once

- Name: Name of the new entity
- Entity: From which entity you want to get the attribute
- Attribute: Which attribute you want as it's own sensor

### Options that you can change at any time

- Icon: Icon to use in frontend
- Device class: Device class (select from list)
- State class: State class (select from list)
- Unit of measurement: UoM to use in frontend (select from list, only temperature, or write your own)

## Installation

### Option 1 (preferred)

Use [HACS](https://hacs.xyz/) to install

### Option 2

Below config-folder create a new folder called`custom_components` if not already exist.

Below new `custom_components` folder create a new folder called `response_as_entity`

Upload the files/folders in `custom_components/response_as_entity` directory to the newly created folder.

Restart before proceeding

## Activate integration in HA

[![Add integrations](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=response_as_entity)

After installation go to "Devices & Services" and then "helper" page in HA, press "+ Create helper" and find "Response as entity"
Follow onscreen information for the required information
No restart needed
