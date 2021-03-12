"""
Module contains classes to describe the context in which AQS data is downloaded
"""


from enum import IntEnum, Enum
from nsaph_utils.utils.context import Context, Argument, Cardinality


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
    This class is part of EPA AQS Toolkit. It allows user to define any
    parameters that are used to select what data to download,
    how to format it and where to place the results.

    It is a concrete subclass of :class Context:
    """

    _years = Argument("years",
                     aliases=['y'],
                     cardinality=Cardinality.multiple,
                     default="1990:2020",
                     help="Year or list of years to download. For example, " +
                        "the following argument: " +
                        "`-y 1992:1995 1998 1999 2011 2015:2017` will produce " +
                        "the following list: " +
                        "[1992,1993,1994,1995,1998,1999,2011,2015,2016,2017]"
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
                          help="Parameter(s) to download, allowed mnemonic " +
                               "names: " + ",".join(list(map(str, Parameter))) +
                               " or integer codes. Example: `-p NO2 44201` " +
                               "will download Ozone and NO2. " +
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

    def __init__(self, doc = None):
        """
        Constructor
        :param doc: Optional argument, specifying what to print as documentation
        """
        self.years = None
        self.parameters = None
        self.aggregation = None
        self.destination = None
        self.merge_years = None
        super().__init__(AQSContext, doc)

    def validate(self, attr, value):
        """
        AQS specific code to handle years and EPA Parameter Codes
        :param attr:
        :param value:
        :return:
        """
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


