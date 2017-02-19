import newspaper
from newspaper import news_pool
import sys
import motor.motor_asyncio
from NewsArticle import NewsArticle
import asyncio


mongoclient = motor.motor_asyncio.AsyncIOMotorClient()
db = mongoclient.newsdb
loop = asyncio.get_event_loop()

async def do_insert(col,doc):
    sz = await col.find({"URL":doc['URL']}).count()
    if sz == 0:
        await col.insert_one(doc)
    else:
        print('B',end="")
    


def get_articles_from(srcs,memoize=True):
    papers = []
    print("Startup, "+str(len(srcs))+" papers to build, download and parse.")
    for s in srcs:
        p = newspaper.build(s,memoize_articles=memoize)
        print(p.domain+" has " +str(p.size())+" new articles")
        if p.size() > 0:
            for i in range(0,p.size()):
                art = p.articles[0]
                art.download()
                if art.is_downloaded:
                    art.parse()
                    if art.is_parsed:
                        art.nlp()
                        na = NewsArticle(art)
                        loop.run_until_complete(do_insert(db[p.domain],na.GetMongoDocument()))
                        print('.',end="",flush=True)
                    else:
                        print(',',end="",flush=True)
                else:
                    print('*',end="",flush=True)
                del p.articles[0]
