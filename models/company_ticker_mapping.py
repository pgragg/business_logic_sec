import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

class CompanyTickerMapping:
    # Reads from a static csv: 'company_ticker_mapping.csv'
    def __init__(self, ticker_mapping=None):
        if( type(ticker_mapping) == pd.core.frame.DataFrame ):
            self.ticker_mapping = ticker_mapping 
        else:
            self.ticker_mapping = pd.read_csv('company_ticker_mapping.csv')
        
    def get(self):
        return self.ticker_mapping
    
    def ticker_symbol_from_cik(self, cik):
        return self.where_equal('cik', cik).ticker_symbol.values[0]
    
    def where_equal(self, column, value):
        df = self.ticker_mapping
        return df.loc[df[column] == value]
    def where_in(self, column, list_of_values):
        df = self.ticker_mapping
        return df.loc[df[column].isin(list_of_values)]