#!/usr/bin/env cwl-runner
### Downloader of AirNow Data

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.airnow]
requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      HTTP_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      HTTPS_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      NO_PROXY: "localhost,127.0.0.1,172.17.0.1"


doc: |
  This tool downloads AirNow data from EPA website

# -p pm25 --dest airnow_pm25.json.gz --from 2020-12-25 --to 2020-12-31 --qc
inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
    inputBinding:
      prefix: --parameters
  from:
    type: string
    doc: Start date for downolading, in YYYY-MM-DD format
    inputBinding:
      prefix: --from
  to:
    type: string
    doc: End date for downolading, in YYYY-MM-DD format
    inputBinding:
      prefix: --to
  cfg:
    type: File
    inputBinding:
      prefix: --cfg
  shapes:
    type: File[]
    inputBinding:
      prefix: --shapes
    secondaryFiles:
      - ".xml"
      - ".iso.xml"
      - ".ea.iso.xml"
      - "^.dbf"
      - "^.sbx"
      - "^.shx"
      - "^.sbn"
      - "^.prj"
      - "^.cpg"
  table:
    type: string
    doc: the name of the table to be created
  api-key:
    type: string?
    inputBinding:
      prefix: --api_key


arguments:
    - valueFrom: "--qc"
    - valueFrom: $(inputs.table + ".json.gz")
      prefix: --destination


outputs:
  log:
    type: File
    outputBinding:
      glob: "*.log"
  data:
    type: File
    outputBinding:
      glob: "*.json*"




