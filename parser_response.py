class ParserResponse:
    def __init__(self) -> None:
        pass
    def extract_phonetic(self,json_data):
        p = None
        a = None
        if "phonetics" in json_data:
            for item in json_data["phonetics"]:
                if "text" in item:
                    p = item["text"]
                    if "audio" in item:
                        a = item["audio"]
                    break
        return p,a
    
    def extract_meaning(self,json_data):
        meanings = []
        
        if "meanings" in json_data:
            for item in json_data["meanings"]:
                pos = None
                definitions = []
                synonyms = []
                antonyms = []
                
                if "partOfSpeech" in item:
                    pos = item["partOfSpeech"]

                for d in item["definitions"]:
                    definitions.append(d["definition"])
                
                if "synonyms" in item:
                    synonyms = item["synonyms"]
                
                if "antonyms" in item:
                    antonyms = item["antonyms"]
                meanings.append(
                    {
                        "pos":pos,
                        "definitions":definitions,
                        "synonyms":synonyms,
                        "antonyms":antonyms
                    }
                )
            
        return meanings

    def parse(self,data):
        try:
            tmp = {}
            
            json_data = data[0]
            
            tmp["word"] = json_data["word"]

            phonetic,audio_url = self.extract_phonetic(json_data)
            
            tmp["phonetic"] = phonetic
            tmp["audio_url"] = audio_url
            
            tmp["meanings"] = self.extract_meaning(json_data)
            return True,tmp
            
        except:
            return False,None