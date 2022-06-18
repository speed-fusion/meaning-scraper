user = "root"
password = "9076b974c31e4678f"
host = "localhost:27017"
database = "multilingual-examples"

import pymongo

class Database:
    def __init__(self):
        db_name = database
        connection_uri = f'mongodb://{user}:{password}@{host}/?authSource=admin'
        client = pymongo.MongoClient(connection_uri)
        db = client[db_name]
        self.en_ar = db["en-ar-words"]
        self.scrape_speed_test = db["scrape-speed-test"]