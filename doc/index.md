# NSAPH EPA Package Description

[Documentation Home](platform-docs:home)

Toolkit for downloading and preprocessing of data provided by EPA

Handles the following types of data: 

* EPA AQS Data hosted at https://www.epa.gov/aqs and EPA AirNow data 
  from https://docs.airnowapi.org/webservices
    * [Pipeline](pipeline/aqs)
* AirNow contains real-time up-to-date pollution data but is less reliable
  than AQS
    * [Pipeline](pipeline/airnow)

## Package Contents

```{toctree}
---
maxdepth: 4
caption: General Description
---
usage
```

```{toctree}
---
maxdepth: 2
caption: Python Components
glob:
---
members/*
```

```{toctree}
---
maxdepth: 2
caption: CWL Tools and Common Workflows
glob:
---
pipeline/*
```

## Indices and tables

* :ref:`genindex`
* :ref:`modindex`
