from config import CONFIG
import requests
import pandas as pd
import time


class ScienceDirect:
    def __init__(self):
        self.query = CONFIG.get("search_query")
        with open("D://scopus_key.txt", "r") as f:
            self.key = f.read().strip()

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
        hit_url = url.format(start, self.query, self.key)
        rainy_day_var = hit_url
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
                last = self.get_last(links)
                if next == last:
                    flag = 0
                    break
                hit_url = next
                rainy_day_var = hit_url
                time.sleep(2)
            except:
                # hit_url = rainy_day_var
                pass
        df.to_csv("SCOPUS_search_results.csv")

    def get_url(self):
        url = "https://api.elsevier.com/content/search/sciencedirect?start={}&count=25" \
              "&query={}&apiKey={}&httpAccept=application%2Fjson"
        return url

    def get(self, hit_url):
        r = requests.get(hit_url)
        return r.json()


if __name__ == '__main__':
    obj = ScienceDirect()
    obj.search()


