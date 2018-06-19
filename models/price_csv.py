import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

import quandl
quandl.ApiConfig.api_key = "Uyaf1-7qy5o9EJt8z_xc"

from .filing_text import FilingText
from .sls_web_httparty import SlsWebHTTParty

class PriceCsv:
    def __init__(self):
        self.range = range(-10, 4)
        
    def get(self, ticker_symbol):
        try:
            return pd.read_csv(f'prices/{ticker_symbol}.csv')
        except:
            return pd.DataFrame.from_dict({})
        
    def update_all(self):
        all_tickers = FilingText().ticker_symbol_dates()
        self.update(all_tickers)
    
    def update(self, list_of_objects=None):
        # If list_of_objects isn't passed in, try to update all prices
        for obj in list_of_objects:
            recent_prices = []
            filing_date = obj['date']
            ticker_symbol = obj['ticker_symbol']
            existing_prices = self.get(ticker_symbol)
            date_range = self.__date_range(filing_date)
            # 'Continue' here if any price in the date_range is in the future 
            if datetime.datetime.strptime(date_range[-1], '%Y-%m-%d') >= datetime.datetime.now():
                print('date is in future')
                continue
            
            # 'Continue' here if date_range is filled in for this ticker_symbol in the csv. 
            if self.__is_in_range(date_range, ticker_symbol):
                print('stock has price data for date range')
                continue
            try:
                recent_prices = self.__av_fetch(date_range, ticker_symbol)
                print("av fetch")
            except:
                recent_prices = []
                time.sleep(1)
#                 try:
#                     recent_prices = self.__quandl_fetch(date_range, ticker_symbol)
#                     print("quandl fetch")
#                 except:
#                     recent_prices = []
            if len(recent_prices) == 0:
                print('fetch failed for ' + ticker_symbol)
                continue
           
            all_prices = recent_prices.append(existing_prices)
            deduped_prices = all_prices.drop_duplicates(subset=['date'])
            beginning_len = len(existing_prices)
            end_len = len(deduped_prices)
            num_updated = str(end_len - beginning_len)
            deduped_prices = deduped_prices.sort_values(by='date')
            deduped_prices.to_csv(f'prices/{ticker_symbol}.csv', index=False)
            print('Successfully updated ' + num_updated + ' dates for ' + ticker_symbol)
        return list_of_objects
    
    def __date_range(self, date):
        dates = []
        for delta in self.range:
            date_delta = datetime.timedelta(days=delta)
            date_string = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            dates.append(str(date_string + date_delta))
        return dates
       
    def __quandl_fetch(self, dates, symbol):
        gte = dates[0]
        lte = dates[-1]
        data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'close', 'open', 'high', 'low'] }, ticker = [symbol], date = { 'gte': gte, 'lte': lte })
        return data
    
    def __av_fetch(self, dates, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=QPL6YTN5VA6V7MP8'
        response = json.loads(SlsWebHTTParty().simple_get(url))
        response = response['Time Series (Daily)']
        records = []
        for date in dates:
            info = response.get(date, {})
            if len(info.keys()) == 0:
                records.append({
                    'date': date,
                    'ticker': symbol,
                    'open': 'N/A',
                    'high': 'N/A',
                    'low': 'N/A',
                    'close': 'N/A'
                 })
                continue
            obj = {
                'date': date,
                'ticker': symbol,
                'open': info['1. open'],
                'high': info['2. high'],
                'low': info['3. low'],
                'close': info['4. close']
            }
            records.append(obj)
        df = pd.DataFrame.from_records(records)
        df = df.sort_values(by='date')
        return df
    
    def __is_in_range(self, date_range, symbol):
        df = self.get(symbol)
        try:
            dates_included_already = len(df.loc[df['date'].isin(date_range)])
        except:
            dates_included_already = 0
        return( dates_included_already == len(date_range) )

