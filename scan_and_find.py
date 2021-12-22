import os
from config import *
import re
import csv
import sys
import pandas as pd


class Searcher:
    def __init__(self, database, path, dois, key):
        self.database = database
        self.path = path
        self.os_list = dois
        self.key = key
        self.rebound_terms = CONFIG.get("rebound_terms")
        self.heuristic = CONFIG.get("heuristic")
        self.data  = self.init_data()
        self.rebound_results = self.init_results()
        self.paper_list = []

    def init_data(self):
        data = {}
        for s in self.heuristic:
            data[s] = 0
        data['total'] = 0
        return data

    def init_results(self):
        data = {}
        for s in self.rebound_terms:
            data[s] = 0
        data['total'] = 0
        return data

    def process(self, s):
        s = re.sub('[^A-Za-z ]', '', s)
        s = re.sub('<[^<]+>', "", s)
        return s.strip().split()

    def setify(self, s):
        return set(s)

    def take_intersection(self, set1, set2):
        return set1.intersection(set2)

    def add_now(self, intersection):
        for i in intersection:
            self.data[i] += 1
        self.data['total'] += 1

    def add_results(self, results):
        for i in results:
            self.rebound_results[i] += 1
        self.rebound_results['total'] += 1

    def write_stuff(self):
        fname = OUTPUT_FILES + "/{}_{}_string_search.csv".format(self.database, self.key)
        f = open(fname, "w", newline='')
        writer = csv.writer(f)
        header = ['Label', 'Number of papers']
        writer.writerow(header)
        writer.writerow(['Total papers searched', len(self.os_list)])
        for i, j in self.data.items():
            row = [i, j]
            writer.writerow(row)
        for i, j in self.rebound_results.items():
            row = [i, j]
            writer.writerow(row)
        f.close()

        fname = OUTPUT_FILES + "/{}_{}_rebound_papers.csv".format(self.database, self.key)
        f = open(fname, "w", newline='')
        writer = csv.writer(f)
        header = ['DOI']
        writer.writerow(header)
        for doi in self.paper_list:
            write_doi = fname_to_doi(doi)
            writer.writerow([write_doi])
        f.close()

    def check_rebound_terms(self, s):
        t = []
        s = " ".join(s)
        for rebound_term in self.rebound_terms:
            if rebound_term in s:
                t.append(rebound_term)
        return t

    def search(self):
        for index, doc in enumerate(self.os_list):
            with open(self.path+"/"+doc, "r", encoding="utf8") as f:
                s = f.read()
                s = s.lower()
                s = self.process(s)
                set_s = self.setify(s)
                intersection = self.take_intersection(set_s, self.heuristic)
                if intersection:
                    self.add_now(intersection)
                    results = self.check_rebound_terms(s)
                    if results:
                        self.add_results(results)
                        self.paper_list.append(doc)
                if index%1000==0:
                    print("{} done.".format(index))
        self.write_stuff()


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
    for search_term in search_terms:
        f = re.sub('[^a-zA-Z]', '', search_term)
        fname = "search_results/{}_{}.csv".format(database, f)
        print("Begin: {}".format(search_term))
        df = pd.read_csv(fname)
        df_dois = set(df['prism:doi'].tolist())
        os_list_dois = set([fname_to_doi(i).replace("DOI:", "") for i in os.listdir(db_dir)])
        dois = df_dois.intersection(os_list_dois)
        dois_file = [doi_to_fname(i) for i in dois]
        print(len(dois))
        obj = Searcher(database, db_dir, dois_file, f)
        obj.search()


