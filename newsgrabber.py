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
    await col.insert_one(doc)


def get_articles_from(srcs):
    papers = []
    print("Startup, "+str(len(srcs))+" papers to build, download and parse.")
    for s in srcs:
        papers.append(newspaper.build(s,memoize_articles=False))
        print(papers[len(papers)-1].domain+" has " +str(papers[len(papers)-1].size())+" new articles")
    for p in papers:
        if p.size() > 0:
            for art in p.articles:
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
