import geopandas
import pandas
from shapely.geometry import Point
from typing import List, Optional


class GISAnnotator:
    def __init__(self, shape_files: List[str], columns: List[str],
                 crs="EPSG:4326"):
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
        self.init()
        actual_n_rows = len(df)
        if actual_n_rows < 1:
            return None
        geometry = [Point(xy) for xy in zip(df[x], df[y])]
        columns = set(self.columns)
        for shapes in self.shapes:
            points = geopandas.GeoDataFrame(df, geometry=geometry, crs=self.crs)
            pts = geopandas.sjoin(points, shapes, how='left')
            cc = {c for c in pts.columns if c in columns}
            ccc = list(df.columns) + list(cc)
            df = geopandas.GeoDataFrame(pts[ccc], geometry=geometry,
                                            crs=self.crs)
            columns -= cc
            if not columns:
                break
        return df

