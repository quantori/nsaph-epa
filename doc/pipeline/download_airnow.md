# Downloader of AirNow Data
**Tool** 	[epa.airnow](../../src/python/epa/airnow.py)

**Source**: [download_airnow.cwl](../../src/cwl/download_airnow.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!-- tocstop -->

## Description
This tool downloads AirNow data from EPA website


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|parameter_code|string| | |
|from|string| | |
|to|string| | |
|cfg|File| | |
|shapes|File[]| | |
|table|string| |the name of the table to be created|
|api-key|string| | |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|data|File| |
