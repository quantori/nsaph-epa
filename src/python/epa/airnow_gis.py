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

import geopandas
import pandas
from shapely.geometry import Point
from typing import List, Optional


class GISAnnotator:
    """
    Geographic Annotator adds columns to a provided data frame
    containing latitude and longitude (or other CRS) with
    labels coming from provided shape files, such as zip
    codes or county names (or FIPS codes) 
    """

    def __init__(self, shape_files: List[str], columns: List[str],
                 crs="EPSG:4326"):
        """
        Create the Annotator

        :param shape_files: list of paths to shape files
        :param columns: List of columns to be added by the annotator
        :param crs:  Coordinate reference system (CRS) used by the input data
        """

        self.shapes = None
        self.shape_files = shape_files
        self.crs = crs
        self.columns = columns

    def init(self):
        if self.shapes:
            return
        self.shapes = [
            geopandas.GeoDataFrame.from_file(f).to_crs(self.crs)
            for f in self.shape_files
        ]

    def join(self, df: pandas.DataFrame, x = "longitude", y = "latitude") \
            -> Optional[pandas.DataFrame]:
        """
        Adds columns with the labels to teh data

        :param df: Incoming data frame
        :param x: A column, containing longitude
        :param y: A column, containing latitude
        :return: data frame with added annotations
        """
        if df.empty:
            return

        self.init()
        geometry = [Point(xy) for xy in zip(df[x], df[y])]
        current_columns = set(self.columns)
        for shapes in self.shapes:
            points = geopandas.GeoDataFrame(df, geometry=geometry, crs=self.crs)
            pts = geopandas.sjoin(points, shapes, how='left')

            founded_columns = set(pts.columns) & current_columns
            target_columns = list(df.columns) + list(founded_columns)

            df = geopandas.GeoDataFrame(pts[target_columns], geometry=geometry, crs=self.crs)
            current_columns -= founded_columns

            if not current_columns:
                break
        return df

