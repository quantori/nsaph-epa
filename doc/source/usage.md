#Usage

    usage: epa.py [-h] [--years [YEARS ...]] [--aggregation {annual,daily}]
                  [--parameters [PARAMETERS ...]] --dest DEST [--merge_years]
    
    optional arguments:
      -h, --help            show this help message and exit
      --years [YEARS ...], -y [YEARS ...]
                            Year or list of years to download, default: 1990:2020
      --aggregation {annual,daily}, -a {annual,daily}
                            Whether to use annual or daily aggregation, default:
                            annual
      --parameters [PARAMETERS ...], -p [PARAMETERS ...]
                            Parameter(s) to download, allowed values:
                            NO2,OZONE,PM25,MAX_TEMP,MIN_TEMP or integer codes.
                            Required for daily data, for annual data defaults to
                            all.
      --dest DEST, -d DEST  Directory to place the downloaded files
      --merge_years         concatenate consecutive years in one file
