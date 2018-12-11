from scrapy.exceptions import DropItem
import pymongo
class TextPipeline(object):
    def __init__(self):
        self.limit = 50
    
    def process_item(self,item,spider):
        # if item['educations']:
        #     for education in item['educations']:
        #         education['school']['introduction']=self.cut(education['school']['introduction'])
        #         education['major']['introduction']=self.cut(education['major']['introduction'])
        #         education['major']['excerpt']=self.cut(education['major']['excerpt'])
        # if item['locations']:
        #     for location in item['locations']:
        #         location['introduction']=self.cut(location['introduction'])
        #         location['excerpt']=self.cut(location['excerpt'])
        # if 'business' in item.keys():
        #     if item['business']:
        #         item['business']['introduction']=self.cut(item['business']['introduction'])
        #         item['business']['excerpt']=self.cut(item['business']['excerpt'])

        return item



    def cut(self, text):
        if len(text) > self.limit:
            text = text[0:self.limit].rstrip()+'...'
        return text


class MongoPipeline(object):
    collection_name = 'users'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True)
        return item
    
    def close_spider(self, spider):
        self.client.close()