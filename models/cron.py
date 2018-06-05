import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

from .sls_web_httparty import SlsWebHTTParty

from .filing_index import FilingIndex
from .filing_text import FilingText
from .price_csv import PriceCsv
from .company_ticker_mapping import CompanyTickerMapping


blacklisted_ciks = ['0001062292']

class Cron:
    def __init__(self, start=0):
        self.start = start
        return None

    def update(self):
        total_updated = 0
        doc_start = 0
        n_updated = FilingIndex(doc_start).update()
        objs_updated = FilingText().update(n_updated)
        prices_updated = PriceCsv().update(objs_updated)
        total_updated = total_updated + len(prices_updated)
        if len(prices_updated) == 0:
            return total_updated
        return total_updated