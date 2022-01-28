import csv
import io
import logging
import sys
import zipfile
from typing import List
import argparse

from epa import PARAMETER_CODE, MONITOR, RECORD
from epa.aqs_tools import transfer
from nsaph_utils.utils.io_utils import fopen

log = logging.getLogger(__name__)

TARGET = "output.csv.gz"


def file_as_stream(filename: str, extension: str = ".csv", params=None, mode=None):
    """
    Returns the content of URL as a stream. In case the content is in zip
    format (excluding gzip) creates a temporary file

    :param mode: optional parameter to specify desirable mode: text or binary.
         Possible values: 't' or 'b'
    :param params: Optional. A dictionary, list of tuples or bytes
         to send as a query string.
    :param filename: path to file
    :param extension: optional, when the content is zip-encoded, the extension
        of the zip entry to return
    :return: Content of the URL or a zip entry
    """
    if filename.lower().endswith(".zip"):
        zfile = zipfile.ZipFile(filename)
        entries = [
            e for e in zfile.namelist() if e.endswith(extension)
        ]
        assert len(entries) == 1
        stream = io.TextIOWrapper(zfile.open(entries[0]))

    else:
        try:
            raw = open(filename, "b").read()
        except IOError as e:
            log.exception("Cannot read %s: %s", filename, e)
            raise

        if mode == 't':
            stream = io.TextIOWrapper(raw)
        else:
            stream = raw

    return stream


def file_as_csv_reader(filename: str):
    """
    An utility method to return the CSV content of the file as CSVReader

    :param filename: path to file
    :return: an instance of csv.DictReader
    """
    stream = file_as_stream(filename)
    reader = csv.DictReader(
        stream, quotechar='"', delimiter=',',
        quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True,
    )
    return reader


def expand_data(files: List[str], parameters: List[int]) -> str:
    log.info("Expand files %r with parameters %r", files, parameters)

    write_header = True
    for filename in files:
        log.info("Process %s", filename)

        with fopen(TARGET, "at") as ostream:
            reader = file_as_csv_reader(filename)

            fieldnames = list(reader.fieldnames)
            fieldnames.append(MONITOR)
            fieldnames.append(RECORD)
            writer = csv.DictWriter(ostream, fieldnames, quotechar='"',
                                    delimiter=',',
                                    quoting=csv.QUOTE_NONNUMERIC)
            if parameters:
                flt = lambda row: int(row[PARAMETER_CODE]) in parameters
            else:
                flt = None
            transfer(reader, writer, flt, write_header)
            write_header = False

    return TARGET


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--parameter_code", dest="parameters", type=int, action='append', required=False, help="Parameter")
    ap.add_argument('files', type=str, nargs='+', help='files to parse')
    args = ap.parse_args()

    expand_data(files=args.files, parameters=args.parameters)
