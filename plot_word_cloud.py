import os
from config import *
import re
import csv
import sys
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
STOPWORDS = stopwords.words('english')
STOPWORDS = STOPWORDS + ['however', 'also', 'et', 'al', 'gif', 'sigif', 'altimg', 'sssigif', 'si', 'svg', 'sisvg']


class PlotWords:
    def __init__(self, database, path, dois):
        self.database = database
        self.path = path
        self.os_list = dois
        self.rebound_terms = CONFIG.get("rebound_terms")
        self.heuristic = CONFIG.get("heuristic")
        self.paper_list = []

    def process(self, s):
        s = re.sub('[^A-Za-z ]', '', s)
        s = re.sub('<[^<]+>', "", s)
        return s.strip().split()

    def plot(self, text):
        #plt.subplots(figsize=(20, 10))
        text = " ".join(text)
        wordcloud = WordCloud(width=1000, height=500, background_color='white', stopwords=STOPWORDS).generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        if database == 'scopus':
            title = database.upper()
        else:
            title='ScienceDirect'
        plt.title(title)
        plt.axis("off")
        plt.savefig("output_images/{}.png".format(database), bbox_inches='tight', dpi=2000)

    def search(self):
        full_text = []
        for index, doc in enumerate(self.os_list):
            with open(self.path+"/"+doc, "r", encoding="utf8") as f:
                s = f.read()
                s = s.lower()
                s = self.process(s)
                full_text.extend(s)
        self.plot(full_text)
        print("Done")


if __name__ == '__main__':

    def fname_to_doi(doi):
        write_doi = "DOI:" + doi.replace('$&$', '/').replace(".txt", '')
        return write_doi

    def doi_to_fname(doi):
        write_doi = doi.replace('/', '$&$').replace("DOI:", "")
        fname = "{}.txt".format(write_doi)
        return fname

    database = sys.argv[1]
    search_terms = CONFIG.get("{}_search_queries".format(database))
    db_dirs = {
        "scopus": "docs_scopus",
        "science_direct": "docs_sd"
    }
    db_dir = db_dirs.get(database)
    fname = "{}_all.csv".format(database)
    print("Begin: {}")
    df = pd.read_csv(fname)
    df_dois = set(df['prism:doi'].tolist())
    os_list_dois = set([fname_to_doi(i).replace("DOI:", "") for i in os.listdir(db_dir)])
    dois = df_dois.intersection(os_list_dois)
    dois_file = [doi_to_fname(i) for i in dois]
    print(len(dois))
    obj = PlotWords(database, db_dir, dois_file)
    obj.search()


