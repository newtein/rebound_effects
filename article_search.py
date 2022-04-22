from config import CONFIG
import requests
import pandas as pd
import time
import sys
import urllib.request as urllib2
import re


class ArticleSearch:
    def __init__(self, database, query, fname):
        self.database = database
        self.query = query
        self.fname = fname

        with open("D://scopus_key.txt", "r") as f:
            self.key = f.readline().strip()
            self.insttoken = f.readline().strip()

    def get_next(self, links):
        for link in links:
            if link.get('@ref') == 'next':
                return link.get('@href')
        return 1

    def get_last(self, links):
        for link in links:
            if link.get('@ref') == 'last':
                return link.get('@href')
        return 0

    def search(self):
        url = self.get_url()
        flag = 1
        start = 0
        hit_url = url.format(start, self.query, self.key, self.insttoken)
        df = pd.DataFrame()
        while flag > 0:
            try:
                print(hit_url)
                result = self.get(hit_url)
                print(result.get("search-results", {}).get("opensearch:startIndex"))
                t_df = pd.DataFrame.from_dict(result.get('search-results', {}).get("entry"))
                df = df.append(t_df)
                links = result.get("search-results", {}).get("link")
                next = self.get_next(links)
                hit_url = next
                time.sleep(4)
            except Exception as e:
                flag = 0
                print(e)
                print(hit_url)

        df.to_csv(self.fname)

    def get_url(self):
        if self.database == 'science_direct':
            url = "https://api.elsevier.com/content/search/sciencedirect?start={}&count=25" \
                  "&query={}&apiKey={}&httpAccept=application%2Fjson&insttoken={}"
        elif self.database == 'scopus':
            url = "https://api.elsevier.com/content/search/scopus?start={}&cursor=*&count=25" \
                  "&query=TITLE-ABS-KEY({})&apiKey={}&httpAccept=application%2Fjson&insttoken={}"
        return url

    def get(self, hit_url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        r = requests.get(hit_url, headers=headers)
        return r.json()


if __name__ == '__main__':
    database = sys.argv[1]
    search_terms = CONFIG.get("{}_search_queries".format(database))
    print(search_terms)
    replace_quotes = {
        '"': "%22",
        ' ': "%20"
    }
    for search_term in search_terms:
        f = re.sub('[^a-zA-Z]', '', search_term)
        fname = "search_results/{}_{}.csv".format(database, f)
        for i, j in replace_quotes.items():
            search_term = search_term.replace(i, j)
        print("Begin {}".format(search_term))
        obj = ArticleSearch(database, search_term, fname)
        obj.search()
        print("Completed {}".format(search_term))


