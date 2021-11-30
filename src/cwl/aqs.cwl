#!/usr/bin/env cwl-runner
### Full Medicaid Processing Pipeline

cwlVersion: v1.2
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}

doc: |
  This workflow downloads AQS data from the government
  servers, introspects it to infer the database schema
  and ingests the data into the database

inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  database:
    type: File
    doc: Path to database connection file, usually database.ini
  connection_name:
    type: string
    doc: The name of the section in the database.ini file
  aggregation:
    type: string
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
  table:
    doc: Name of the table to be created in the database
    type: string

steps:
  states:
    run: ensure_resource.cwl
    doc: |
      Ensures the presence of `us_states` table in the database.
      The table contains mapping between state names, ids
      (two letter abbreviations), FIPS codes and
      [ISO-3166-2 codes](https://en.wikipedia.org/wiki/ISO_3166-2)
    in:
      database: database
      connection_name: connection_name
      table:
        valueFrom: "us_states"
    out: [log]
  iso:
    run: ensure_resource.cwl
    doc: |
      Ensures the presence of `us_iso` table in the database.
      The table provides a mapping between states, counties and zip
      codes. It contains FIPS and
      [ISO-3166-2 codes](https://en.wikipedia.org/wiki/ISO_3166-2)
    in:
      database: database
      connection_name: connection_name
      table:
        valueFrom: "us_iso"
    out: [log]

  download:
    run: download_aqs.cwl
    in:
      aggregation: aggregation
      parameter_code: parameter_code
      proxy: proxy
    out: [log, data, errors]

  introspect:
    run: introspect.cwl
    in:
      depends_on: download/log
      input: download/data
      table: table
      output:
        valueFrom: epa.yaml
    out: [log, model, errors]

  ingest:
    run: ingest.cwl
    doc: Uploads data into the database
    in:
      registry: introspect/model
      table: table
      input: download/data
      database: database
      connection_name: connection_name
    out: [log, errors]

  index:
    run: index.cwl
    in:
      depends_on: ingest/log
      registry: introspect/model
      domain:
        valueFrom: "epa"
      table: table
      database: database
      connection_name: connection_name
    out: [log]


outputs:
  resource1_log:
    type: File
    outputSource: states/log
  resource2_log:
    type: File
    outputSource: iso/log
  download_log:
    type: File
    outputSource: download/log
  introspect_log:
    type: File
    outputSource: introspect/log
  ingest_log:
    type: File
    outputSource: ingest/log
  index_log:
    type: File
    outputSource: index/log
  data:
    type: File
    outputSource: download/data
  model:
    type: File
    outputSource: introspect/model
  download_err:
    type: File
    outputSource: download/errors
  introspect_err:
    type: File
    outputSource: introspect/errors
  ingest_err:
    type: File
    outputSource: ingest/errors
