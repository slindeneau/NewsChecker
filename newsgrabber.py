import newspaper
from newspaper import news_pool
import sys
import motor.motor_asyncio
from NewsArticle import NewsArticle
import asyncio
from multiprocessing import Pool
from urllib.parse import urlparse



mongoclient = motor.motor_asyncio.AsyncIOMotorClient()
db = mongoclient.newsdb
loop = asyncio.get_event_loop()

async def do_insert(col,doc):
    sz = await col.find({"URL":doc['URL']}).count()
    if sz == 0:
        await col.insert_one(doc)
        print('.',end="",flush=True)
    else:
        print('-',end="",flush=True)
    


def get_articles_from(srcs,memoize=True,pool_size=2):
    papers = []
    workers = Pool(processes=pool_size)
    print("Startup, "+str(len(srcs))+" papers to build, download and parse.")
    for s in srcs:
        p = newspaper.build(s,memoize_articles=memoize)
        print("\n"+p.domain+" has " +str(p.size())+" new articles")
        if p.size() > 0:
            workers.map(get_article,p.articles)
            #for i in range(0,p.size()):
            #    art = p.articles[0]
            #    del p.articles[0]

def get_article(art):
    art.download()
    if art.is_downloaded:
        art.parse()
        if art.is_parsed:
            art.nlp()
            na = NewsArticle(art)
            p_uri = urlparse(art.source_url)
            p_domain = '{uri.netloc}'.format(uri=p_uri)
            loop.run_until_complete(do_insert(db[p_domain],na.GetMongoDocument()))
        else:
            print(',',end="",flush=True)
    else:
        print('*',end="",flush=True)
