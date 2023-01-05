import rasterio
from rasterio import plot as rasterplot
from rasterio.mask import mask
from shapely.geometry import mapping
from rasterio import Affine
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import os


class HighestElevationLocator(object):

    def __init__(self, dem_path, study_area):
        self.dem_path = dem_path
        self.study_area = study_area

    def masking(self):
        geoms = [mapping(self.study_area)]
        with rasterio.open(self.dem_path, 'r') as src:
            out_image, out_transform = mask(src, geoms, crop=True)
        return out_image, out_transform

    def data_extraction(self):
        with rasterio.open(self.dem_path, 'r') as src:
            out_meta = src.meta.copy()
            out_image, out_transform = self.masking()
            out_meta.update({
                'driver': 'GTiff'
                , 'height': out_image.shape[1]
                , 'width': out_image.shape[2]
                , 'transform': out_transform
            })

            root = os.path.dirname(os.getcwd())
            out_file_path = os.path.join(root, 'Material', 'outputs', 'masked_raster.tif')
            with rasterio.open(out_file_path, 'w', **out_meta) as out_file:
                out_file.write(out_image)

        return out_file_path

    def highest_locator(self, masked_image_path):
        evacu_points = []
        with rasterio.open(masked_image_path, 'r') as masked_raster:
            band_data = masked_raster.read(1) # this is in type array
            evacu_record = np.where(band_data == np.amax(band_data))
            evacu_point_xy = masked_raster.xy(evacu_record[0], evacu_record[1])
            evacu_point = Point(evacu_point_xy[0][0], evacu_point_xy[1][0])
            evacu_points.append((evacu_point.x, evacu_point.y))

        return evacu_points

