import pandas as pd
import requests
import time


class ArticleContent:
    def __init__(self, database, path):
        self.database = database
        self.path = path
        self.fname = "{}_search_results.csv".format(self.database)
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

    def execute(self):
        dois = self.df['prism:doi'].tolist()
        not_found = open("{}_not_found.csv".format(self.database), "w")
        for index, doi in enumerate(dois):
            if index >= 3195:
                url = self.get_url()
                url = url.format(doi, self.key, self.insttoken)
                print(url)
                r = self.get(url)
                full_text = self.get_content(r)
                print(doi)
                if full_text:
                    write_doi = doi.replace('/', '$&$').replace("DOI:", "")
                    fname = "{}/{}.txt".format(self.path, write_doi)
                    f = open(fname, "wb")
                    f.write(full_text.encode('utf-8'))
                    f.close()
                else:
                    not_found.write("{}\n".format(doi))
                time.sleep(3)


        not_found.close()


    def get(self, hit_url):
        r = requests.get(hit_url)
        return r.json()

    def get_url(self):
        if self.database == 'science_direct':
            url = "https://api.elsevier.com/content/article/doi/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        elif self.database == 'scopus':
            url = "https://api.elsevier.com/content/abstract/doi/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"

        #url = "https://api.elsevier.com/content/article/scopus_id/{}?apiKey={}&insttoken={}&httpAccept=application%2Fjson"
        return url

if __name__ == '__main__':
    obj = ArticleContent('scopus', 'docs_scopus')
    obj.execute()
