from temporal_article_search import GetTotal
import time
import sys
import pandas as pd
from config import *


class TemporalPatterns:
    def __init__(self, database):
        self.search_strings = {
            "science_direct": [
       "\"\\\"smart home\\\" OR \\\"smart home\\\"\"",
        "\"\\\"energy efficiency\\\" OR \\\"energy efficient\\\"\"",
        "\"\\\"rebound effect\\\" OR \\\"rebound effects\\\" OR \\\"jevons paradox\\\" OR \\\"khazzoom-brookes postulate\\\"\"",
        "\"(\\\"smart home\\\" OR \\\"smart home\\\") AND (\\\"energy efficiency\\\" OR \\\"energy efficient\\\")\"",
        "\"(\\\"smart home\\\" OR \\\"smart home\\\") AND (\\\"rebound effect\\\" OR \\\"rebound effects\\\" OR \\\"jevons paradox\\\" OR \\\"khazzoom-brookes postulate\\\")\"",
        "\"(\\\"energy efficiency\\\" OR \\\"energy efficient\\\") AND (\\\"rebound effect\\\" OR \\\"rebound effects\\\" OR \\\"jevons paradox\\\" OR \\\"khazzoom-brookes postulate\\\")\"",
       "\"(\\\"smart home\\\" OR \\\"smart home\\\") AND (\\\"energy efficiency\\\" OR \\\"energy efficient\\\") AND (\\\"rebound effect\\\" OR \\\"rebound effects\\\" OR \\\"jevons paradox\\\" OR \\\"khazzoom-brookes postulate\\\")\""
        ],
            "scopus": [
        '"smart home*"',
        '"energy efficien*"',
        '"rebound effect" OR "rebound effects" OR "jevons paradox" OR "khazzoom-brookes postulate"',
        '"smart home*" AND "energy efficien*"',
        '"smart home*" AND ("rebound effect" OR "rebound effects" OR "jevons paradox" OR "khazzoom-brookes postulate")',
        '"energy efficien*" AND ("rebound effect" OR "rebound effects" OR "jevons paradox" OR "khazzoom-brookes postulate")',
        '"energy efficien*" AND "smart home*" AND ("rebound effect" OR "rebound effects" OR "jevons paradox" OR "khazzoom-brookes postulate")',
        ]
        }
        self.science_direct_search_queries = self.search_strings.get(database)
        self.search_labels = ["S", "E", "R", "ES", "SR", "ER", "ESR"]

    def execute(self, syear, eyear):
        rows = []
        years = list(map(lambda x:str(x), list(range(syear, eyear+1))))
        club_years = ["{}-{}".format(years[i], years[i+1]) for i in range(len(years)-1)]
        print(club_years)
        for search_term, search_label in zip(self.science_direct_search_queries, self.search_labels):
            for year in club_years:
                print(year)
                obj = GetTotal(database, search_term, "{}_all.csv".format(database), 0, year)
                print(search_label, obj.search())
                time.sleep(2)
                rows.append([year, search_label, obj.search()])

        df = pd.DataFrame(data=rows, columns=["year", "search", "count"])
        df.to_csv(OUTPUT_FILES+"/temporal_{}_{}_{}.csv".format(database, syear, eyear), index=False)


if __name__ == '__main__':
    database = sys.argv[1]
    obj = TemporalPatterns(database)
    obj.execute(2011,2021)