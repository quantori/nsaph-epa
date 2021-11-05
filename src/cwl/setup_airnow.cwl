#!/usr/bin/env cwl-runner
### Prepare environment for AirNow

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.airnow_setup]

doc: |
  This tool prepares environemnt for AirNow download
  It checks that AirNow API key is provided and installs
  zip and county shape files if necessary

inputs:
  api-key:
    type: string
    inputBinding:
      position: 1

outputs:
  cfg:
    type: File
    outputBinding:
      glob: ".airnow.yaml"
  shapes:
    type: Directory
    outputBinding:
      glob: "shapes"
  log:
    type: stdout

stdout: setup.log





