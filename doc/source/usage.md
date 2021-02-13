EPA AQS Toolkit Usage
=====================
        
    python -m aqs [-h] 
        [--years [YEARS ...]] 
        [--aggregation {annual,daily}] 
        --parameters PARAMETERS [PARAMETERS ...] 
        --destination DESTINATION 
        [--merge_years]
    
    optional arguments:
      -h, --help            show this help message and exit
      --years [YEARS ...], -y [YEARS ...]
                            Year or list of years to download. For example, the
                            following argument: `-y 1992:1995 1998 1999 2011
                            2015:2017` will produce the following list:
                            [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017],
                            default: 1990:2020
      --aggregation {annual,daily}, -a {annual,daily}
                            Whether to use annual or daily aggregation, default:
                            annual
      --parameters PARAMETERS [PARAMETERS ...], -p PARAMETERS [PARAMETERS ...]
                            Parameter(s) to download, allowed mnemonic names:
                            NO2,OZONE,PM25,MAX_TEMP,MIN_TEMP or integer codes.
                            Example: `-p NO2 44201` will download Ozone and NO2.
                            Required for daily data, for annual data defaults to
                            all.
      --destination DESTINATION, --dest DESTINATION, -d DESTINATION
                            Destination directory for the downloaded files
      --merge_years         Concatenate consecutive years in one file, default:
                            False
