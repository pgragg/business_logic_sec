import os 
import glob as glob
from bs4 import BeautifulSoup as Soup
from tqdm import tqdm
import codecs

class DataCleaner:
    def __init__(self):
        return None
    
    def clean_texts(self):
        # Removes html from all texts in filing_texts and 
        # writes the cleaned file to proc_filing_texts
        
        # Files written
        successes = 0
        # Parsing errors 
        errors    = 0
        # Empty files (another kind of parsing error)
        zeroes    = 0
        
        filename_candidates = [filepath.split('/')[-1] for filepath in glob.glob('filing_texts/*')]
        filenames_already_written = [filepath.split('/')[-1] for filepath in glob.glob('proc_filing_texts/*')]
        filenames_to_write = [filename for filename in filename_candidates if filename not in filenames_already_written]
        
        # Don't worry about files which are already written
        for filename in tqdm(filenames_to_write):
            try:
                sf = self.__stringify_file(f'filing_texts/{filename}')
                if len(sf) == 0:
                    zeroes += 1
                    continue
                f = open(f'proc_filing_texts/{filename}', 'w+')
                f.write(sf)
                f.close()
                successes += 1
            except: 
                errors += 1

        print(f'Successes: {successes}')
        print(f'Errors: {errors}')
        print(f'Zeroes: {zeroes}')
    
    def __stringify_file(self, filename):
        res = codecs.open(filename, "r",encoding='utf-8', errors='ignore').read()
        soup = Soup(res,'html.parser')
        text = []
        for p in soup.find_all('p'):
            text.append(p.text.replace("\\n", ' -_n_- '))
        string = ' '.join(text)
        return string.encode('utf-8', "backslashreplace").decode('utf-8')