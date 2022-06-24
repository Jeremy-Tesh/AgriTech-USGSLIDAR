import pandas as pd
from urllib.request import urlopen
from constants import state_mapper
from dateutil.parser import parse
import json

class Fetch:
    def __init__(self) -> None:
        pass

    def fetch_metadata(filename):
        """
        extracts metadata from the public usgs lidar url 
        args: str 
            filename - this is where you will save your file data
        return: df
            returns a dataframe containing the metadata specified
        """
        data = []
        
        for _,state in state_mapper.items():
            url = f"https://s3-us-west-2.amazonaws.com/usgs-lidar-public/{state}/ept.json"
                        
            response = None
            # store the response of URL
            try:
                response = urlopen(url)
            except Exception as e:
                print(e)
            
            if response:
                # storing the JSON response 
                json_obj = json.loads(response.read())
                lc = {}
                # access properties from this file
                lc['state_description'] = state
                
                try:
                    
                    lc['year'] = parse(state,fuzzy=True).year
                    lc['points'] = json_obj['points']
                    lc['bounds'] = json_obj['bounds']
                    lc['X'] = json_obj['schema'][0]['offset']
                    lc['Y'] = json_obj['schema'][1]['offset']
                    lc['Z'] = json_obj['schema'][2]['offset']
                    lc['EPSG'] = json_obj['srs']['authority']
                    lc['EPSG_Output'] = json_obj['srs']['horizontal']

                except Exception as e:
                    
                    lc['year'] = 1000
                
                data.append(lc)
                    
        df=pd.DataFrame(data)    
        
        df.to_csv(filename,index=False)
        
        return df

fetch = Fetch()