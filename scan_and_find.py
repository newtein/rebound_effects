import os
from config import *
import re
import csv


class Searcher:
    def __init__(self, database, path):
        self.database = database
        self.path = path
        self.os_list = os.listdir(self.path)
        self.rebound_terms = CONFIG.get("rebound_terms")
        self.heuristic = CONFIG.get("heuristic")
        self.data = self.init_data()
        self.paper_list = []

    def init_data(self):
        data = {}
        for s in self.heuristic:
            data[s] = 0
        data['total'] = 0
        return data

    def process(self, s):
        s = re.sub('[^A-Za-z ]', '', s)
        return s.strip().split()

    def setify(self, s):
        return set(s)

    def take_intersection(self, set1, set2):
        return set1.intersection(set2)

    def add_now(self, intersection):
        for i in intersection:
            self.data[i] += 1
        self.data['total'] += 1

    def write_stuff(self):
        fname = OUTPUT_FILES + "/{}_string_search.csv".format(self.database)
        f = open(fname, "w", newline='')
        writer = csv.writer(f)
        header = ['Label', 'Number of papers']
        writer.writerow(header)
        writer.writerow(['Total papers searched', len(self.os_list)])
        for i, j in self.data.items():
            row = [i, j]
            writer.writerow(row)
        f.close()

        fname = OUTPUT_FILES + "/{}_rebound_papers.csv".format(self.database)
        f = open(fname, "w", newline='')
        writer = csv.writer(f)
        header = ['DOI']
        writer.writerow(header)
        for doi in self.paper_list:
            write_doi = "DOI:" + doi.replace('$&$', '/').replace(".txt", '')
            writer.writerow([write_doi])
        f.close()

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
                    self.paper_list.append(doc)
                if index%1000==0:
                    print("{} done.".format(index))
        self.write_stuff()


if __name__ == '__main__':
    # obj = Searcher("scopus", "docs_scopus")
    obj = Searcher("science_direct", "docs_sd")
    obj.search()


