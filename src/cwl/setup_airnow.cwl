#!/usr/bin/env cwl-runner
### Prepare environment for AirNow

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.airnow_setup]
requirements:
  InlineJavascriptRequirement: {}

doc: |
  This tool prepares environemnt for AirNow download
  It checks that AirNow API key is provided and installs
  zip and county shape files if necessary

inputs:
  api-key:
    type: string
    inputBinding:
      position: 1
  shape_dir:
    type: Directory?
    inputBinding:
      position: 2
  cfg:
    type: File?
    inputBinding:
      position: 3


outputs:
  cfg:
    type: File
    outputBinding:
      glob: ".airnow.yaml"
#  shape_dir:
#    type: Directory
#    outputBinding:
#      glob: "shapes"
  shapes:
    type: File[]
    outputBinding:
      glob: "shapes/*.shp"
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
  log:
    type: stdout

stdout: setup.log





