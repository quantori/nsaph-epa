"""
    Geographic Annotator annotates data frame containing
    latitude and longitude with
    labels coming from provided shape files, such as zip
    codes or county names (or FIPS codes)
"""


#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import csv
import os
from typing import List

import geopandas
import pandas
from numpy import nan
from shapely.geometry import Point


class GISAnnotator:
    """
    Geographic Annotator adds columns to a provided data frame
    containing latitude and longitude (or other CRS) with
    labels coming from provided shape files, such as zip
    codes or county names (or FIPS codes) 
    """
    ZIP_COLUMNS = {"ZCTA"}
    COUNTY_COLUMNS = {"STATEFP", "COUNTYFP"}
    CALCULATED_COLUMNS = {"COUNTY", "STUSPS", "STATEISO", "STATE", "FIPS5"}

    def __init__(self, shape_files: List[str], columns: List[str],
                 crs="EPSG:4326"):
        """
        Create the Annotator

        :param shape_files: list of paths to shape files
        :param columns: List of columns to be added by the annotator
        :param crs:  Coordinate reference system (CRS) used by the input data
        """
        if set(columns) - (self.ZIP_COLUMNS | self.COUNTY_COLUMNS | self.CALCULATED_COLUMNS):
            raise ValueError("Unknown requested columns")

        self.shape_files = shape_files
        self.crs = crs
        self.columns = columns

        self.zip_shapes = None
        self.county_shapes = None
        self._states = dict()

    def join(self, df: pandas.DataFrame, x="longitude", y="latitude") \
            -> pandas.DataFrame:
        """
        Adds columns with the labels to teh data

        :param df: Incoming data frame
        :param x: A column, containing longitude
        :param y: A column, containing latitude
        :return: data frame with added annotations
        """
        if df.empty:
            return df

        self._load_shape_files()
        self._check_columns()

        geometry = [Point(xy) for xy in zip(df[x], df[y])]

        if self.zip_shapes is not None:
            df = self._add_shape_columns(df, geometry, self.zip_shapes, self.ZIP_COLUMNS)

        if self.county_shapes is not None:
            df = self._add_shape_columns(df, geometry, self.county_shapes, self.COUNTY_COLUMNS)

        self._add_calculated_columns(df)

        return df

    def _check_columns(self):
        if (set(self.columns) & self.ZIP_COLUMNS) and self.zip_shapes is None:
            raise ValueError("ZIP column is requested, but no zip shape file found")

        if (set(self.columns) & self.COUNTY_COLUMNS) and self.county_shapes is None:
            raise ValueError("County columns are requested, but no county shape file found")

    def _load_shape_files(self):
        if self.zip_shapes is not None or self.county_shapes is not None:
            return

        for filename in self.shape_files:
            data = geopandas.GeoDataFrame.from_file(filename).to_crs(self.crs)

            if "ZIP" in data.columns:
                print("MATCH ZIP")
                data.rename(columns={'ZIP': 'ZCTA'}, inplace=True)
                self.zip_shapes = data

            elif "ZCTA5CE10" in data.columns:
                print("MATCH ZCTA")
                data.rename(columns={'ZCTA5CE10': 'ZCTA'}, inplace=True)
                self.zip_shapes = data

            elif "STATEFP" in data.columns and "COUNTYFP" in data.columns:
                print("MATCH COUNTY")
                self.county_shapes = data

    def _add_shape_columns(
            self,
            df: pandas.DataFrame,
            geometry: List,
            shape: geopandas.GeoDataFrame,
            shape_columns: set
    ) -> geopandas.GeoDataFrame:
        # join incoming data with polygons
        points = geopandas.GeoDataFrame(df, geometry=geometry, crs=self.crs)
        pts = geopandas.sjoin(points, shape, how='left')

        # drop all columns except of requested
        target_columns = list(df.columns) + list(set(self.columns) & shape_columns)
        df = geopandas.GeoDataFrame(pts[target_columns], geometry=geometry, crs=self.crs)

        return df

    def _add_calculated_columns(self, df: pandas.DataFrame) -> None:
        if "STATEFP" not in df.columns:
            return

        if "COUNTY" in self.columns:
            df["COUNTY"] = [
                state_fp + county_fp if state_fp is not nan else None
                for state_fp, county_fp in zip(df["STATEFP"], df["COUNTYFP"])
            ]

        if "FIPS5" in self.columns:
            df["FIPS5"] = [
                state_fp + county_fp if state_fp is not nan else None
                for state_fp, county_fp in zip(df["STATEFP"], df["COUNTYFP"])
            ]

        if "STATE" in self.columns:
            df["STATE"] = [
                state_fp if state_fp is not nan else None
                for state_fp in df["STATEFP"]
            ]

        if "STUSPS" in self.columns:
            df["STUSPS"] = [
                self._get_state_by_fips(state_fp)["STUSPS"] if state_fp is not nan else None
                for state_fp in df["STATEFP"]
            ]

        if "STATEISO" in self.columns:
            df["STATEISO"] = [
                "US-" + self._get_state_by_fips(state_fp)["STUSPS"] if state_fp is not nan else None
                for state_fp in df["STATEFP"]
            ]

    def _get_state_by_fips(self, fips: str) -> dict:
        if not self._states:
            self._read_states()

        return self._states[fips]

    def _read_states(self):
        states_filename = os.path.join(os.path.dirname(__file__), "states.csv")
        with open(states_filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')

            for state in reader:
                self._states[state["STATEFP"]] = state
