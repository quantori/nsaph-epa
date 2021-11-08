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
|aggregation|string| | |
|parameter_code|string| | |

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|data|File| |
