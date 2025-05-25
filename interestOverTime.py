from typing import List
from pytrends.request import TrendReq
import pandas as pd
import random 

def interest_over_time(kwords: List[str] = [], tframe = 'all', geo = ''):
    """Takes a list of keywords to check, and returns a dataframe 
    of interest over time to the current day."""

    try:
        #initialize the pytrends in english
        pt = TrendReq()
        
        #build the payload with the list of strings that were input
        pt.build_payload(kw_list=kwords, timeframe=tframe, geo=geo)

        #Collect the data for trends
        data = pt.interest_over_time()

        #remove the ispartial col
        if not data.empty:
            data = data.drop(columns='isPartial')

        #return the dataframe
        return data
    
    except Exception as e:
        print(f'ERROR: {e}')
        return pd.DataFrame()
