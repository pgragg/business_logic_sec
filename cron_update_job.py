from models.cron import Cron
import time 

if __name__ == "__main__":
    for i in range(86400): # should run for days
        print('Retrieved ' + str(Cron().update()) + ' new filings' )
        time.sleep(360)
        