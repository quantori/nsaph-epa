# Prepare environment for AirNow
**Tool** 	[epa.airnow_setup](../../src/python/epa/airnow_setup.py)

**Source**: [setup_airnow.cwl](../../src/cwl/setup_airnow.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!-- tocstop -->

## Description
This tool prepares environemnt for AirNow download
It checks that AirNow API key is provided and installs
zip and county shape files if necessary


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|api-key|string| | |
|shape_dir|Directory| | |
|cfg|File| | |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|cfg|File| |
|shapes|File[]| |
|log|stdout| |
