import gensim
import gensim.models.keyedvectors as word2vec

# our classes
import blobRepo
import Db
from PreprocessText import PlainTextPreprocessor

model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
i2w = model.wv.index2word

def identify_topics(num_topics=5, no_below=3, no_above=.34, passes=50):
    #create topics based on lemma lists created from whole files
    
    trained_bigram_model = gettrained_bigram_model()

    lemmas = []
    for datafile in blobRepo.BlobRepo.GetBlobs(blobRepo.BlobRepo):
        try:
            #get the tokens and bigrams
            tokens = PlainTextPreprocessor.getTokens(PlainTextPreprocessor, datafile)
            tokens_and_bigrams = PlainTextPreprocessor.getNGrams(PlainTextPreprocessor, PlainTextPreprocessor.getBigramList(PlainTextPreprocessor, tokens), trained_bigram_model)

            #clean up the tokens
            #we leave the bigrams, b/c they are unlikely to be in the stop word list and this will speed it up
            lemmas.append()                
        except Exception as e :
            print(e)
            continue

    #create and filter dictionary
    dictionary = gensim.corpora.Dictionary(lemmas)
    #dictionary.append(getbigram(lemmas))
    dictionary.filter_extremes(no_below=no_below, 
                               no_above=no_above)
    
    #Use dictionary to form bag of words
    bow_corpus = [dictionary.doc2bow(doc) for doc in lemmas]
    
    #Fit tfidf model
    tfidf = gensim.models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    lda_model_tfidf = gensim.models.LsiModel(corpus_tfidf, 
                                             #num_topics=num_topics, 
                                             id2word = dictionary 
                                             #passes = passes
                                             )
    return(lda_model_tfidf, dictionary)

#todo need to move this to factory so we can have custom models for bigrams
def gettrained_bigram_model():
    raw_list = list(filter(lambda s: '_' in s, i2w ))
    return [tup for tup in raw_list if len(tup)> 0]

if __name__ == "__main__":
    identify_topics(num_topics=20, no_above=.95, no_below=.25)