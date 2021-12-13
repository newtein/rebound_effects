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
        dois = self.df['dc:identifier'].tolist()
        path = "docs_sd"
        not_found = open("Science_direct_not_found.csv", "w")
        for index, doi in enumerate(dois):
            if index >= 2152:
                url = self.get_url()
                url = url.format(doi, self.key, self.insttoken)
                print(url)
                r = self.get(url)
                full_text = r.get("full-text-retrieval-response", {}).get('originalText')
                print(doi)
                if full_text:
                    write_doi = doi.replace('/', '$&$').replace("DOI:", "")
                    fname = "{}/{}.txt".format(path, write_doi)
                    f = open(fname, "wb")
                    try:
                        f.write(full_text.encode('utf-8'))
                    except:
                        print(full_text)
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
        #url = "https://api.elsevier.com/content/article/scopus_id/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        return url

if __name__ == '__main__':
    obj = ScopusFullText("science_direct_search_results.csv")
    obj.execute()
