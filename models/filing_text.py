import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

from .company_ticker_mapping import CompanyTickerMapping
from .filing_index import FilingIndex
from .sls_web_httparty import SlsWebHTTParty


class FilingText:
    def __init__(self):
        return None
    
    # Saves the document text of the last n filings to the local filing_texts folder
    def update(self, num=-1):
        updated = []
        # Write each filing to file
        for filing in self.ticker_symbol_dates(num):
            ticker_symbol = filing['ticker_symbol']
            date =  filing['date']
            filename = filing['filename']
            link = filing['link']
            if os.path.isfile(filename):
                continue
            else:
                updated.append(filing)
                doc_text = str(SlsWebHTTParty().simple_get(filing['link']))
                f = open(filename,'w')
                f.write(doc_text)
                f.close()
        return updated
    
    def ticker_symbol_dates(self, num=-1):
        tm = CompanyTickerMapping().get()
        # Get a list of ciks that we have stock ticker symbols for
        ciks = tm.cik 
        # Find recent filings 
        filings = FilingIndex().get()[:num]
        fwks = filings.loc[filings['cik'].isin(ciks.values)]
        output = []
        # Write each filing to file
        for filing in fwks.to_records():
            ticker_symbol = CompanyTickerMapping(ticker_mapping=tm).ticker_symbol_from_cik(filing.cik)
            date = str(filing.updated).split('T')[0]
            filename = f'filing_texts/{ticker_symbol}_{date}'
            output.append({'ticker_symbol': ticker_symbol, 'date': date, 'filename': filename, 'link': filing.link})
        return output
    
    def missing_ticker_symbol_dates(self, num=-1):
        tm = CompanyTickerMapping().get()
        # Get a list of ciks
        ciks = tm.cik 
        # Find recent filings 
        filings = FilingIndex().get()[:num]
        # Return filings we don't have ciks for 
        fwks = filings.loc[~filings['cik'].isin(ciks.values)]
        return fwks