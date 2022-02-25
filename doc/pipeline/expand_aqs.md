# Downloader of AQS Data
**Tool** 	[epa.aqs_expand](../../src/python/epa/aqs_expand.py)

**Source**: [expand_aqs.cwl](../../src/cwl/expand_aqs.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!-- tocstop -->

## Description
This tool adds additional columns (i.e. record id) to AQS data

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|parameter_code|string| |Parameter code. Either a numeric code (e.g. 88101, 44201) or symbolic name (e.g. PM25, NO2). See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|data|File| |
|errors|stderr| |
