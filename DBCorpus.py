from NewsArticle import NewsArticle
import motor.motor_asyncio
import asyncio
import gensim
import nltk
from nltk.tokenize import RegexpTokenizer

mongoclient = motor.motor_asyncio.AsyncIOMotorClient()
db = mongoclient.newsdb
loop = asyncio.get_event_loop()
tokenizer = RegexpTokenizer(r'\w+')

async def get_colnames():
    return await db.collection_names(False)

async def do_find(col,q):
    cursor = col.find({})
    return await cursor.to_list(None)

async def do_size(col):
    return await col.find({}).count()


class DBCorpus(gensim.corpora.TextCorpus):
    colnames = loop.run_until_complete(get_colnames())

    def get_texts(self):
        for cn in DBCorpus.colnames:
            docs = loop.run_until_complete(do_find(db[cn],{}))
            for d in docs:
                text = d["Text"].replace('\n',' ').lower()
                text = text.replace("'s","")
                text = text.replace("'","")
                text = text.replace(",","")
                text = [tokenizer.tokenize(line) for line in nltk.sent_tokenize(text) if len(line) > 0]
                yield text #broken up into sentences
                #yield [item for sublist in text for item in sublist] #one continuous document
                #for line in text:  #one line at a time
                #    yield line 

    def __len__(self):
        """Define this so we can use `len(corpus)`"""
        self.length = 0
        for cn in DBCorpus.colnames:
            self.length = self.length + loop.run_until_complete(do_size(db[cn]))
        return self.length

