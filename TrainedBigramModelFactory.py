import gensim.models.keyedvectors as word2vec

model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
i2w = model.wv.index2word


class BigramModelFactory:

    def gettrained_bigram_model():
        raw_list = list(filter(lambda s: '_' in s, i2w ))
        return [tup for tup in raw_list if len(tup)> 0]
