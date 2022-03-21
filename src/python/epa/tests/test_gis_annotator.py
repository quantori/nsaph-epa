import geopandas
import pandas
import pytest
from numpy import isnan
from shapely.geometry import Polygon

from .. import airnow_gis


@pytest.fixture()
def zip_shape():
    coordinates = Polygon([
        (40, -102),
        (36, -102),
        (36, -95),
        (40, -95),
    ])

    df = pandas.DataFrame(data=[1], columns=['ZCTA'])
    shape = geopandas.GeoDataFrame(data=df, geometry=[coordinates])
    return shape


def test_state():
    annotator = airnow_gis.GISAnnotator([], [])
    state = annotator._get_state_by_fips('09')
    assert state == {
        'STATEFP': '09',
        'STATENS': '01779780',
        'STUSPS': 'CT',
        'NAME': 'Connecticut',
    }


def test_columns():
    with pytest.raises(ValueError) as e:
        airnow_gis.GISAnnotator(shape_files=[], columns=['xx'])

    assert e.value.args[0] == 'Unknown requested columns'


def test_no_zip():
    annotator = airnow_gis.GISAnnotator(shape_files=[], columns=['ZCTA'])
    annotator.county_shapes = "placeholder"

    df = pandas.DataFrame([1], columns=['Column'])

    with pytest.raises(ValueError) as e:
        annotator.join(df=df)

    assert e.value.args[0] == 'ZIP column is requested, but no zip shape file found'


def test_no_county():
    annotator = airnow_gis.GISAnnotator(shape_files=[], columns=['COUNTYFP'])
    annotator.zip_shapes = "placeholder"

    df = pandas.DataFrame([1], columns=['Column'])

    with pytest.raises(ValueError) as e:
        annotator.join(df=df)

    assert e.value.args[0] == 'County columns are requested, but no county shape file found'


def test_join_found(zip_shape):
    annotator = airnow_gis.GISAnnotator(shape_files=[], columns=['ZCTA'])
    annotator.zip_shapes = zip_shape

    df = pandas.DataFrame(data=[['001', 38, -100]], columns=['column', 'longitude', 'latitude'])
    result = annotator.join(df)

    assert result.iloc[0]['ZCTA'] == 1


def test_join_not_found(zip_shape):
    annotator = airnow_gis.GISAnnotator(shape_files=[], columns=['ZCTA'])
    annotator.zip_shapes = zip_shape

    df = pandas.DataFrame(data=[['001', 50, -100]], columns=['column', 'longitude', 'latitude'])
    result = annotator.join(df)

    assert isnan(result.iloc[0]['ZCTA'])
