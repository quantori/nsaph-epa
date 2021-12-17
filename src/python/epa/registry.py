"""
Creates Registries (YAML schemas) for EPA data by introspecting
downloaded files
"""

import os
from typing import Dict

import yaml

from nsaph import init_logging
from nsaph.loader.introspector import Introspector
from nsaph_utils.utils.context import Context, Argument, Cardinality

from epa import RECORD

DOMAIN_NAME = "epa"


class EPAConfig(Context):

    _output = Argument("output",
            help = "Output path for schema",
            type = str,
            default = DOMAIN_NAME,
            cardinality = Cardinality.single
        )

    _data = Argument("data",
            help = "Path to a data file to introspect",
            type = str,
            required = True,
            default = None,
            cardinality = Cardinality.single
        )

    _table = Argument("table",
            help = "Name of the table",
            type = str,
            required = True,
            default = None,
            cardinality = Cardinality.single
        )

    def __init__(self, doc):
        self.output = None
        ''' Output path for schema '''
        self.data = None
        ''' Path to a data file to introspect '''
        self.table = None
        ''' Name of the table '''
        super().__init__(EPAConfig, doc, include_default = False)


class Registry:
    """
    This class parses File Transfer Summary files and
    creates YAML data model. It can either
    update built-in registry or write
    the model to a designated path
    """

    def __init__(self, context: EPAConfig = None):
        init_logging()
        if not context:
            context = EPAConfig(__doc__).instantiate()
        self.context = context
        self.domain = None

    def update(self):
        registry_path = self.context.output
        if os.path.isfile(registry_path):
            with open(registry_path, "rt") as f:
                self.domain = yaml.safe_load(f)
        else:
            self.domain = self.create_domain_yaml()
        self.create_table_yaml()
        with open(registry_path, "wt") as f:
            yaml.dump(self.domain, stream=f)
        return

    @staticmethod
    def create_domain_yaml() -> Dict:
        domain = {
            DOMAIN_NAME: {
                "reference": "https://www.epa.gov/aqs",
                "schema": DOMAIN_NAME,
                "index": "selected",
                "header": True,
                "tables": {
                }
            }
        }
        return domain

    def create_table_yaml(self):
        table = dict()
        introspector = Introspector(self.context.data)
        introspector.introspect()
        columns = introspector.get_columns()
        table["columns"] = columns
        table["primary_key"] = [
            RECORD
        ]
        self.domain[DOMAIN_NAME]["tables"][self.context.table] = table


if __name__ == '__main__':
    Registry().update()
    