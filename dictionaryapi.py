import scrapy
from database import Database

from parser_response import ParserResponse

from pipeline import DictionaryApiPipeline

from scrapy.crawler import CrawlerProcess

import os

from datetime import datetime

class DictionaryApiScraper(scrapy.Spider):
    
    name = 'dictionary-api-scraper'
    
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    db = Database()
    
    p = ParserResponse()
    
    proxy = os.environ.get("PROXY",None)
    
    headers = {
    'authority': 'api.dictionaryapi.dev',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    
    def start_requests(self):
        
        for word in list(self.db.scrape_speed_test.find({}).limit(1)):
            
            url = self.url + word["word"]
            
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                method="GET",
                meta= {
                    "word":word,
                    "proxy":self.proxy
                },
                callback=self.parse_response
            )
    
    def to_json(self,response):
        try:
            json_data = response.json()
            return json_data
        except:
            return None
    
    def parse_response(self,response):
        
        word = response.meta["word"]
        
        item = {}
        item["status"] = 0
        item["data"] = {}
        item["word"] = word
        
        json_data = self.to_json(response)
        
        if json_data == None:
            print(f'dictionary api does not have any data for word {word["word"]}')
            
            item["status"] = 0
            
        else:
            status,data = self.p.parse(json_data)
            
            if status == False:
                item["status"] = 0
            else:
                item["status"] = 2
                
                item["data"] = data
                
        yield item
        


if __name__ == "__main__":
    
    settings = {
        "ROBOTSTXT_OBEY":False,
        "ITEM_PIPELINES":{
            DictionaryApiPipeline:300
        },
        'CONCURRENT_REQUESTS_PER_DOMAIN':40,
        'CONCURRENT_REQUESTS':40,
        'CONCURRENT_ITEMS':200,
        'RETRY_ENABLED':True,
        'RETRY_TIMES':3,
        'RETRY_HTTP_CODES':[403],
        'COOKIES_ENABLED':False
        
    }
    
    c = CrawlerProcess(settings)
    
    c.crawl(DictionaryApiScraper)
    
    t1 = datetime.now()
    c.start()
    t2 = datetime.now()
    
    print(f'total time : {(t2 - t1).seconds}')