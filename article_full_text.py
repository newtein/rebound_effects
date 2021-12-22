import pandas as pd
import requests
import time
import sys
from config import CONFIG
import re
import os


class ArticleContent:
    def __init__(self, database, path, fname):
        self.database = database
        self.path = path
        self.fname = fname
        self.df = pd.read_csv(self.fname)
        with open("D://scopus_key.txt", "r") as f:
            self.key = f.readline().strip()
            self.insttoken = f.readline().strip()

    def get_content(self, r):
        if self.database == 'science_direct':
            full_text = r.get("full-text-retrieval-response", {}).get('originalText')
        elif self.database == 'scopus':
            full_text = r.get("abstracts-retrieval-response", {}).get('coredata', {}).get('dc:description', {})
        return full_text

    def get_filename(self, doi):
        write_doi = doi.replace('/', '$&$').replace("DOI:", "")
        fname = "{}/{}.txt".format(self.path, write_doi)
        return fname

    def execute(self):
        self.df = self.df[~pd.isna(self.df['prism:doi'])]
        dois = self.df['prism:doi'].tolist()
        not_found = open("{}_not_found.csv".format(self.database), "a")
        for index, doi in enumerate(dois):
            url = self.get_url()
            url = url.format(doi, self.key, self.insttoken)
            fname = self.get_filename(doi)
            if not os.path.exists(fname):
                print(url)
                try:
                    r = self.get(url)
                except:
                    time.sleep(2)
                    r = self.get(url)
                full_text = self.get_content(r)
                if full_text:
                    try:
                        f = open(fname, "wb")
                        f.write(full_text.encode('utf-8'))
                        f.close()
                    except:
                        print(full_text)
                else:
                    not_found.write("{}\n".format(doi))
                time.sleep(3)
            else:
                print("Found {}/{}".format(doi, fname))
        not_found.close()


    def get(self, hit_url):
        session = requests.Session()
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        r = session.get(hit_url, headers=headers)
        return r.json()

    def get_url(self):
        if self.database == 'science_direct':
            url = "https://api.elsevier.com/content/article/doi/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        elif self.database == 'scopus':
            url = "https://api.elsevier.com/content/abstract/doi/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"

        #url = "https://api.elsevier.com/content/article/scopus_id/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        return url

if __name__ == '__main__':
    database = sys.argv[1]
    search_terms = CONFIG.get("{}_search_queries".format(database))
    db_dirs = {
        "scopus": "docs_scopus",
        "science_direct": "docs_sd"
    }
    db_dir = db_dirs.get(database)
    for search_term in search_terms:
        f = re.sub('[^a-zA-Z]', '', search_term)
        fname = "search_results/{}_{}.csv".format(database, f)
        print("Begin: {}".format(search_term))
        obj = ArticleContent(database, db_dir, fname)
        obj.execute()
        print("Completed: {}".format(search_term))
