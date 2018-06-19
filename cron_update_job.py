from models.cron import Cron
from models.data_cleaner import DataCleaner
import time 

if __name__ == "__main__":
    for i in range(86400): # should run for days
        print('Retrieved ' + str(Cron().update()) + ' new filings' )
        DataCleaner().clean_texts()
        time.sleep(360)
        
