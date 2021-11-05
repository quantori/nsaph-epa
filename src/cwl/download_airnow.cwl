#!/usr/bin/env cwl-runner
### Downloader of AirNow Data

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.airnow]
requirements:
  InlineJavascriptRequirement: {}


doc: |
  This tool downloads AirNow data from EPA website

# -p pm25 --dest airnow_pm25.json.gz --from 2020-12-25 --to 2020-12-31 --qc
inputs:
  parameter_code:
    type: string
    inputBinding:
      prefix: --parameters
  from:
    type: string
    inputBinding:
      prefix: --from
  to:
    type: string
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




