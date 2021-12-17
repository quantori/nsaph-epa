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
|proxy|string|``|HTTP/HTTPS Proxy if required|
|parameter_code|string| |Parameter code. Either a numeric code (e.g. 88101, 44201) or symbolic name (e.g. PM25, NO2). See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list) |
|from|string| |Start date for downolading, in YYYY-MM-DD format|
|to|string| |End date for downolading, in YYYY-MM-DD format|
|cfg|File| | |
|shapes|File[]| | |
|table|string| |the name of the table to be created|
|api-key|string| | |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|data|File| |
