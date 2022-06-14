# Index Builder
**Tool** 	[nsaph.loader.index_builder](../../../../platform/doc/members/index_builder.html)

**Source**: [index.cwl](../../src/cwl/index.cwl)

<!--TOC-->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)

<!--TOC-->

## Description
This tool builds all indices for the specified table.
Log file displays real-time progress of building indices


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|registry|File| |A path to the data model file |
|table|string| |the name of the table|
|database|File| |Path to database connection file, usually database.ini|
|connection_name|string| |The name of the section in the database.ini file|
|depends_on|File| |a special field used to enforce dependencies and execution order|

## Outputs

| Name | Type | Description |
|------|------|-------------|
|log|File| |
