#!/usr/bin/env cwl-runner
### Downloader of AQS Data

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.aqs]

requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      HTTP_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      HTTPS_PROXY: "$('proxy' in inputs? inputs.proxy: null)"
      NO_PROXY: "localhost,127.0.0.1,172.17.0.1"


doc: |
  This tool downloads AQS data from EPA website

# --dest /Users/misha/harvard/projects/epa/aqs -p PM25 -a annual --merge_years
inputs:
  proxy:
    type: string?
    default: ""
    doc: HTTP/HTTPS Proxy if required
  aggregation:
    type: string
    inputBinding:
      prefix: --aggregation
    doc: "Aggregation type: annual or daily"
  parameter_code:
    type: string
    doc: |
      Parameter code. Either a numeric code (e.g. 88101, 44201)
      or symbolic name (e.g. PM25, NO2).
      See more: [AQS Code List](https://www.epa.gov/aqs/aqs-code-list)
    inputBinding:
      prefix: --parameters

arguments:
    - valueFrom: "--merge_years"


outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  data:
    type: File?
    outputBinding:
      glob: "*.csv*"
  errors:
    type: stderr

stderr: download.err




