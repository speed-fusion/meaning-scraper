import scrapy
from database import Database

from parser_response import ParserResponse

from pipeline import DictionaryApiPipeline

from scrapy.crawler import CrawlerProcess

import os

class DictionaryApiScraper(scrapy.Spider):
    
    name = 'dictionary-api-scraper'
    
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    db = Database()
    
    p = ParserResponse()
    
    proxy = os.environ.get("PROXY",None)
    
    def start_requests(self):
        
        for word in list(self.db.scrape_speed_test.find({}).limit(1000)):
            
            url = self.url + word["word"]
            
            yield scrapy.Request(
                url=url,
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
    
    c.start()