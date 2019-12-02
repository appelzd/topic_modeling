import gensim
import gensim.models.keyedvectors as word2vec

# our classes
import blobRepo
import Db
from PreprocessText import PlainTextPreprocessor
from bigram_model_repo import bigram_model_repo

# model=word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)  
# i2w = model.wv.index2word

def identify_topics(num_topics=5, no_below=3, no_above=.34, passes=50):
    #create topics based on lemma lists created from whole files
    
    #seriaize
    blob = blobRepo.BlobRepo()
    preprocess = PlainTextPreprocessor()
    bigram_repo = bigram_model_repo()

    lemmas = []
    for datafile in blob.GetBlobs():
        try:
            #get the tokens and bigrams
            tokens = preprocess.getTokens( datafile)
            tokens_and_bigrams = preprocess.getNGrams(preprocess.getBigramList(datafile), bigram_repo.getBigramModel())

            #clean up the tokens
            tokens = preprocess.removeStopWords(tokens)
            lemmas = preprocess.getLemmas(preprocess.getPartsofSpeech(tokens))

            #we leave the bigrams, b/c they are unlikely to be in the stop word list and this will speed it u
            lemmas.append(tokens_and_bigrams)                
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

if __name__ == "__main__":
    lda_model, dictionary = identify_topics(num_topics=20, no_above=.95, no_below=.25)

    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} ".format(idx))
        print("Word: {} ".format(topic))
        print("\n")
        #writeToDb(topic)
        
    for tp in topic_prediction:
        print('Test file likely to be topic {}, probability = {:.4f}'.format(tp[0][0], tp[0][1]))