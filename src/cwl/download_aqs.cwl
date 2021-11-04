#!/usr/bin/env cwl-runner
### Downloader of AQS Data

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.aqs]

doc: |
  This tool downloads AQS data from EPA website

# --dest /Users/misha/harvard/projects/epa/aqs -p PM25 -a annual --merge_years
inputs:
  aggregation:
    type: string
    inputBinding:
      prefix: --aggregation
  parameter_code:
    type: string
    inputBinding:
      prefix: --parameters

arguments:
    - valueFrom: "--merge_years"


outputs:
  log:
    type: File
    outputBinding:
      glob: "*.log"
  data:
    type: File
    outputBinding:
      glob: "*.csv*"




