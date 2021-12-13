# Introspector for downloaded data file
**Tool** 	[epa.registry](../../src/python/epa/registry.py)

**Source**: [introspect.cwl](../../src/cwl/introspect.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!-- tocstop -->

## Description
This tool examines a directory with downlaoded
EPA data and generates a table defintion


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|input|File| |A path the downloaded data file |
|output|string| |A path to a file name with EPA data model|
|table|string| |the name of the table to be created|
|depends_on|File| |a special field used to enforce dependencies and execution order|

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
|model|File| |
|errors|stderr| |
