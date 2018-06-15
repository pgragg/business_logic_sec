import pandas as pd

from models.filing_text import FilingText
from models.price_csv import PriceCsv

    
if __name__ == "__main__":
    num = len(pd.read_csv('company_ticker_mapping.csv'))
    objs_updated = FilingText().update(n_updated)
    prices_updated = PriceCsv().update(objs_updated)
    print('Retrieved ' + str(objs_updated) + ' new filing_texts' )
