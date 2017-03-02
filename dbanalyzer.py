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
    
colnames = loop.run_until_complete(get_colnames())
sentences = []
for cn in colnames:
    docs = loop.run_until_complete(do_find(db[cn],{}))
    words = []
    for d in docs:
        text = d["Text"].replace('\n',' ').lower()
        text = text.replace("'s","")
        text = text.replace("'","")
        words = words + [tokenizer.tokenize(line) for line in nltk.sent_tokenize(text) if len(line) > 0]
    print(cn + " "+str(len(words)))
    sentences = sentences + words

print("Total sentences: " + str(len(sentences)))
print("Training")
model = gensim.models.Word2Vec(sentences,workers=4,size=1000)
model.save('testmodel')
