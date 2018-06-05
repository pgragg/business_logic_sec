import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

from .recent_forms import RecentForms

class FilingIndex:
    def __init__(self, start=0):
        self.start = start
        return None
    
    # Gets recent forms idempotently and saves to filings_index.csv
    def update(self):
        filings_index_df = self.get()
        recent_filings_df = RecentForms(self.start).get_all()
        all_filings = recent_filings_df.append(filings_index_df)
        deduped_filings = all_filings.drop_duplicates(subset=['link'])
        new_filing_count = len(deduped_filings) - len(filings_index_df)
        deduped_filings.to_csv('filings_index.csv', index=False)
        return new_filing_count
    
    def get(self):
        try:
            return pd.read_csv('filings_index.csv')
        except: 
            return pd.DataFrame.from_dict({})