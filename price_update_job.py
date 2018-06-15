from models.price_csv import PriceCsv
import time 

if __name__ == "__main__":
  for i in range(15):
    print(str(PriceCsv().update_all()))
    time.sleep(360)
        