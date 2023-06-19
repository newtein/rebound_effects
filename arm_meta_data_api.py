from config import CONFIG
import requests
import pandas as pd
import time
import sys
import urllib.request as urllib2
import re


class IEEE:
    def __init__(self, query, year):
        self.query = query
        self.syear, self.eyear = year.split('-')

        with open("C://Keys/ieee_key.txt", "r") as f:
            self.key = f.readline().strip()


    def search(self):
        url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext={}&apikey={}&start_year={}&end_year={}".format(
            self.query, self.key, self.syear, self.syear)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Content-Type': 'application/json',
        }
        r = requests.get(url, headers=headers)
        out = r.json()
        return out.get('total_records')




if __name__ == '__main__':
    obj = database = GetTotal("smart homes", 2018)
    print(obj.hit())
