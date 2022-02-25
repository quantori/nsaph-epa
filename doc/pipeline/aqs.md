# Full Medicaid Processing Pipeline
**Workflow**

**Source**: [aqs.cwl](../../src/cwl/aqs.cwl)

<!-- toc -->

- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Steps](#steps)

<!-- tocstop -->

## Description
This workflow downloads AQS data from the government
servers, introspects it to infer the database schema
and ingests the data into the database


## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
|proxy|string|``|HTTP/HTTPS Proxy if required|
|database|File| |Path to database connection file, usually database.ini|
|connection_name|string| |The name of the section in the database.ini file|
|aggregation|string| | |
|parameter_code|string| |Parameter code. Either a numeric code (e.g. 88101, 44201) or symbolic name (e.g. PM25, NO2). See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list) |
|table|string| |Name of the table to be created in the database|

## Outputs

| Name | Type | Description |
|------|------|-------------|
|resource1_log|File| |
|resource2_log|File| |
|download_log|File| |
|introspect_log|File| |
|ingest_log|File| |
|index_log|File| |
|data|File| |
|model|File| |
|download_err|File| |
|introspect_err|File| |
|ingest_err|File| |

## Steps

| Name       | Runs                                      | Description                                                                                                                                                                                                            |
|------------|-------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| states     | [ensure_resource.cwl](ensure_resource.md) | Ensures the presence of `us_states` table in the database. The table contains mapping between state names, ids (two letter abbreviations), FIPS codes and [ISO-3166-2 codes](https://en.wikipedia.org/wiki/ISO_3166-2) |
| iso        | [ensure_resource.cwl](ensure_resource.md) | Ensures the presence of `us_iso` table in the database. The table provides a mapping between states, counties and zip codes. It contains FIPS and [ISO-3166-2 codes](https://en.wikipedia.org/wiki/ISO_3166-2)         |
| download   | [download_aqs.cwl](download_aqs.md)       |                                                                                                                                                                                                                        |
| expand     | [expand_aqs.cwl](expand_aqs.md)           | Adds additional columns to csv                                                                                                                                                                                         |
| introspect | [introspect.cwl](introspect.md)           |                                                                                                                                                                                                                        |
| ingest     | [ingest.cwl](ingest.md)                   | Uploads data into the database                                                                                                                                                                                         |
| index      | [index.cwl](index.md)                     |                                                                                                                                                                                                                        |
