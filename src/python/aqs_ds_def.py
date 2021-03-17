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
    '''NO2'''
    OZONE = 44201
    '''ozone'''
    PM25 = 88101
    '''PM25'''
    MAX_TEMP = 68104
    '''maximum temperature'''
    MIN_TEMP = 68103
    '''minimum temperature'''

    def __str__(self):
        return str(self.name)

    @classmethod
    def values(cls):
        return {p.value for p in Parameter}


class Aggregation(Enum):
    """An Enum used to specify how the data is aggregated in time"""

    ANNUAL = "annual"
    '''annual aggregation'''
    DAILY = "daily"
    '''daily aggregation'''


class AQSContext(Context):
    """
    This class is part of EPA AQS Toolkit. It allows user to define any
    parameters that are used to select what data to download,
    how to format it and where to place the results.

    It is a concrete subclass of :class Context:
    """

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

        self.parameters = None
        '''Parameters (variables, e.g. PM25, NO2, etc.) to download'''
        self.aggregation = None
        '''Aggregation: daily or annual'''
        self.destination = None
        '''Destination directory for the downloaded files'''
        self.merge_years = None
        '''Whether to concatenate consecutive years in one file'''
        super().__init__(AQSContext, doc)

    def validate(self, attr, value):
        """
        AQS specific code to handle years and EPA Parameter Codes

        :param attr:
        :param value:
        :return:
        """

        value = super().validate(attr, value)
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


