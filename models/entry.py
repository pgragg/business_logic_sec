import pandas as pd
import numpy as np
import os
import json
import glob
import datetime
import time

class Entry:
    # Wraps Soup objects with an interface that gives info on that form. 
    def __init__(self, soup_entry):
        self.entry = soup_entry
        return None
        
    def title(self):
        title_text = self.entry.find('title').get_text()
        return title_text.split('(')[0].split('-')[-1].strip().upper()
    
    def cik(self):
        title_text = self.entry.find('title').get_text()
        cik = '0'
        for spltxt in title_text.split('(')[1:]:
            try:
                str(int(spltxt[0]))
                cik = spltxt.split(')')[0]
            except:
                continue
        return cik
        
    def link(self):
        return self.entry.find('link').get_attribute_list('href')[0].replace('-index.htm', '.txt')
        
    def summary(self):
        text = self.entry.find('summary').get_text()
        return ' --- '.join(text.split('<br>')[1:]).replace("\n", '')
        
    def updated(self):
        return self.entry.find('updated').get_text()
    
    def to_dict(self):
        return {
            'title': self.title(),
            'cik': self.cik(),
            'link': self.link(),
            'summary': self.summary(),
            'updated': self.updated()
        }