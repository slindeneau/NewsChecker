
print("Startup...")

import gensim
import DBCorpus


print("Connecting to corpus")
dbc = DBCorpus.DBCorpus()
print("Corpus Size: "+str(len(dbc)))

print("Using Word2Vec model from ./testmodel")
model = gensim.models.Word2Vec.load('testmodel')

print("Building Index")
index = gensim.similarities.WmdSimilarity(dbc, model, num_best=5) # build the index
print("Index Built")

#model = gensim.models.Word2Vec(sentences,workers=4)
#model.save('testmodel')

