# Downloader of AQS Data
**Tool** 	[epa.aqs](../../src/python/epa/aqs.py)

**Source**: [download_aqs.cwl](../../src/cwl/download_aqs.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!-- tocstop -->

## Description
This tool downloads AQS data from EPA website


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|proxy|string|``|HTTP/HTTPS Proxy if required|
|aggregation|string| |Aggregation type: annual or daily|
|parameter_code|string| |Parameter code. Either a numeric code (e.g. 88101, 44201) or symbolic name (e.g. PM25, NO2). See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|data|File| |
|errors|stderr| |
