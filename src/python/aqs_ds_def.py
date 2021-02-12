from enum import IntEnum, Enum
from internal.context import Context, Argument, Cardinality


class Parameter(IntEnum):
    """
    An Enum with mnemonic names for the most common EPA AQS Parameter Codes
    See more at https://www.epa.gov/aqs/aqs-code-list
    """
    NO2 = 42602
    OZONE = 44201
    PM25 = 88101
    MAX_TEMP = 68104
    MIN_TEMP = 68103

    def __str__(self):
        return str(self.name)

    @classmethod
    def values(cls):
        return {p.value for p in Parameter}


class Aggregation(Enum):
    """An Enum used to specify how the data is aggregated in time"""
    ANNUAL = "annual"
    DAILY = "daily"


class AQSContext(Context):
    """
    Utility to download EPA AQS Data hosted at https://www.epa.gov/aqs
    """

    _years = Argument("years",
                     aliases=['y'],
                     cardinality=Cardinality.multiple,
                     default="1990:2020",
                     help="Year or list of years to download"
                     )
    _aggregation = Argument("aggregation",
                           aliases=['a'],
                           cardinality=Cardinality.single,
                           default="annual",
                           help="Whether to use annual or daily aggregation",
                           valid_values=[a.value for a in Aggregation]
                           )
    _parameters = Argument("parameters",
                          aliases=['p'],
                          cardinality=Cardinality.multiple,
                          help="Parameter(s) to download, allowed values: " +
                               ",".join(list(map(str, Parameter))) +
                               " or integer codes. " +
                               "Required for daily data, for annual data " +
                               "defaults to all."
                          )
    _destination = Argument("destination",
                           aliases=['dest', 'd'],
                           cardinality=Cardinality.single,
                           help="Destination directory for the downloaded files"
                           )
    _merge_years = Argument("merge_years",
                           type=bool,
                           help="Concatenate consecutive years in one file"
                           )

    def __init__(self):
        self.years = None
        self.parameters = None
        self.aggregation = None
        self.destination = None
        self.merge_years = None
        super().__init__(AQSContext)

    def validate(self, attr, value):
        value = super().validate(attr, value)
        if attr == "years":
            years = []
            for y in value:
                if ':' in y:
                    x = y.split(':')
                    y1 = int(x[0])
                    y2 = int(x[1])
                    years += range(y1, y2 + 1)
                else:
                    years.append(int(y))
            return sorted(years)
        if attr == "aggregation":
            return Aggregation(value)
        if attr == "parameters":
            parameters = []
            if value:
                for p in value:
                    if p.isnumeric():
                        parameters.append(int(p))
                    else:
                        parameters.append(self.enum(Parameter, p))
            return parameters
        return value


