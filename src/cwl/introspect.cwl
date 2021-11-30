#!/usr/bin/env cwl-runner
### Introspector for downloaded data file

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, epa.registry]

doc: |
  This tool examines a directory with downlaoded
  EPA data and generates a table defintion


inputs:
  input:
    type: File
    inputBinding:
      prefix: --data
    doc: |
      A path the downloaded data file
  output:
    type: string
    doc: A path to a file name with EPA data model
    inputBinding:
      prefix: --output
  table:
    type: string
    doc: the name of the table to be created
    inputBinding:
      prefix: --table
  depends_on:
    type: File?
    doc: a special field used to enforce dependencies and execution order

outputs:
  log:
    type: File?
    outputBinding:
      glob: "*.log"
  model:
    type: File?
    outputBinding:
      glob: "*.yaml"
  errors:
    type: stderr

stderr: introspect.err

