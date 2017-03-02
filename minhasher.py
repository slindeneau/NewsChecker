
print("Startup...")

from datasketch import MinHashLSH, MinHash
import DBCorpus


print("Connecting to corpus")
dbc = DBCorpus.DBCorpus()
print("Corpus Size: "+str(len(dbc)))

lsh = MinHashLSH(threshold=0.9, num_perm=512)
print("Generating minhashes")
i = 0
for doc in dbc.get_texts():
    mh = MinHash(num_perm=512)
    for line in doc:
        for word in line:
            mh.update(word.encode('utf-8'))
    lsh.insert(str(i),mh)
    i = i + 1
    if i%100 == 0:
        print(".",end="",flush=True)


print("\nDone")

for doc in dbc.get_texts():
    mh = MinHash(num_perm=512)
    for line in doc:
        for word in line:
            mh.update(word.encode('utf-8'))
    results = lsh.query(mh)
    if(len(results) > 3 && len(results) < 10):
        print(results)
        break
