import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

from bs4 import BeautifulSoup as Soup
from .entry import Entry
from .sls_web_httparty import SlsWebHTTParty

class RecentForms:
    # Used by FilingIndex to get recent forms
    def __init__(self, start=0, count=100):
        rss = """https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent
                 &CIK=&type=8-K&company=&dateb=&owner=exclude&start="""
        rss = rss + str(start) + "&count="
        rss = rss + str(count) + "&output=atom"
        res = SlsWebHTTParty().simple_get(rss)
        soup = Soup(res,'xml')
        self.entries = soup.find_all('entry')
        
    def get_all(self):
        return pd.DataFrame.from_records([Entry(entry).to_dict() for entry in self.entries])
