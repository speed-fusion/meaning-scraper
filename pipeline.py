from database import Database

class DictionaryApiPipeline:
    def __init__(self) -> None:
        self.db = Database()
        
        
    def process_item(self,item,spider):
        
        id = item["word"]["_id"]
        
        data = item["data"]
        
        data["status"] = item["status"]
        
        self.db.all_words.update_one(
                {"_id":id},
                {
                    "$set":data
                }
            )
        
        return item