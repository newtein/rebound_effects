import pandas as pd
import requests
import time


class ScopusFullText:
    def __init__(self, fname):
        self.fname = fname
        self.df = pd.read_csv(fname)
        with open("D://scopus_key.txt", "r") as f:
            self.key = f.readline().strip()
            self.insttoken = f.readline().strip()

    def execute(self):
        dois = self.df['prism:doi'].tolist()
        url = self.get_url()
        path = "docs"
        not_found = open("SCOPUS_not_found.csv", "w")
        for doi in dois:
            url = url.format(doi, self.key, self.insttoken)
            print(url)
            r = self.get(url)
            full_text = r.get("full-text-retrieval-response", {}).get('originalText')
            print(doi)
            if full_text:
                write_doi = doi.replace('/', '$&$')
                fname = "{}/{}.txt".format(path, write_doi)
                f = open(fname, "w")
                f.write(full_text)
                f.close()
            else:
                not_found.write("{}\n".format(doi))
            time.sleep(3)

        not_found.close()


    def get(self, hit_url):
        r = requests.get(hit_url)
        return r.json()

    def get_url(self):
        url = "https://api.elsevier.com/content/article/doi/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        return url

if __name__ == '__main__':
    obj = ScopusFullText("Scopus_search_results.csv")
    obj.execute()
