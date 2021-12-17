#!/usr/bin/env cwl-runner
### Downloader of AQS Data
#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

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




