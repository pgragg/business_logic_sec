import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

from requests import get
from requests.exceptions import RequestException
from contextlib import closing

class SlsWebHTTParty:
    def __init__(self):
        return None
    
    def simple_get(self, url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None
        """
        try:
            with closing(get(url, stream=True)) as resp:
                return resp.content

        except RequestException as e:
            log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


    def log_error(self, e):
        """
        It is always a good idea to log errors. 
        This function just prints them, but you can
        make it do anything.
        """
        print(e)