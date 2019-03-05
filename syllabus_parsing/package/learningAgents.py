from model import Model
from documentCleaner import DocumentCleaner
import gensim
import pandas as pd


class LdaAgent(Model):


    def __init__(self, documents):
        self.number_of_topics = 0
        self.documents = documents
        self.cleaned_documents = [DocumentCleaner().clean_document(document, english = True, return_list = True, stopwords = True) 
                                for document in self.documents]
        self.id2word = gensim.corpora.Dictionary(self.cleaned_documents)
        self.bag_of_words_per_document = [self.id2word.doc2bow(document) for document in self.cleaned_documents]
        

    def __get_lda_topics(self, num_topics, use_tfidf):
        if not use_tfidf:
            model = gensim.models.ldamodel.LdaModel(self.bag_of_words_per_document, num_topics=20, id2word=self.id2word, passes=50)
        else:
            tfidf = models.TfidfModel(bow_corpus)
            corpus_tfidf = tfidf[bow_corpus]
            model = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=10, id2word=id2word, passes=50)
        word_dict = {}
        for i in range(num_topics):
            words = model.show_topic(i, topn = 20)
            word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words]
        return pd.DataFrame(word_dict)
            

    def train(self, num_topics, use_tfidf=False):
        return self.__get_lda_topics(num_topics, use_tfidf)

        

class NmfAgent(Model):

    def train(self, num_topics):
        pass


class HdaAgent(Model):

    def train(self, num_topics):
        pass
