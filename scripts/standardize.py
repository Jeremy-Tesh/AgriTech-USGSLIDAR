import numpy as np
import geopandas as gpd
import pandas as pd
from scipy.interpolate import griddata

class Standardizer(object):

    def __init__(self) -> None:
        pass

    def by_distance(self,distance,results):
        """

        interpolate data by elevation from distance to grid
        
        args: 
            distance (int): distance between the spaces
        
        return:
            list of tuples in the format (X,Y,Z)
        """
        long = [x[0] for x in results]
        lat = [x[1] for x in results]
        x = [(long[i],lat[i])for i in range(len(long))]
        y = [x[2] for x in results]
        evaluate_at = x[::distance]   
        interpolated_data = griddata(x, y, evaluate_at) 
        interpolated_list = [(evaluate_at[i]+(interpolated_data[i],))for i in range(len(evaluate_at))]
        df = pd.DataFrame({'elevation_m':interpolated_data})
        interpolated_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy([x[0] for x in evaluate_at], 
                                                            [x[1] for x in evaluate_at]))
        return interpolated_list,interpolated_gdf

standardize = Standardizer()