from model import Model
from documentCleaner import DocumentCleaner
import gensim
import pandas as pd
from pdftextExtractor import PDFTextExtractor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
import pickle

class LdaAgent(Model):


    def __init__(self, topn=20, documents=None):
        Model.__init__(self)
        self.topn = topn
        self.documents = documents        
        self.preprocess(self.documents)


    def __get_lda_topics(self, num_topics, use_tfidf):
        if not use_tfidf:
            model = gensim.models.ldamodel.LdaModel(self.bag_of_words_per_document, num_topics, id2word=self.id2word, passes=50)
        else:
            tfidf = gensim.models.TfidfModel(self.bag_of_words_per_document)
            corpus_tfidf = tfidf[self.bag_of_words_per_document]
            model = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics, id2word=self.id2word, passes=50)
        self.trained_model = model
        return self.extract_topics_from_trained_model(num_topics)


    def extract_topics_from_trained_model(self, num_topics):
        if self.trained_model:
            word_dict = {}
            for i in range(num_topics):
                words = self.trained_model.show_topic(i, topn = self.topn)
                word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words]
            return pd.DataFrame(word_dict)
        return None


    def preprocess(self, documents):
        if documents:
            self.cleaned_documents = [DocumentCleaner().clean_document(document, english = True, return_list = True, stopwords = True) 
                                    for document in self.documents]
            self.id2word = gensim.corpora.Dictionary(self.cleaned_documents)
            self.bag_of_words_per_document = [self.id2word.doc2bow(document) for document in self.cleaned_documents]


    def train(self, num_topics, use_tfidf=False):
        results = self.__get_lda_topics(num_topics, use_tfidf)
        self.last_trained_results = results
        return results


    def transform_unseen_document(self, document):
        cleaned_document = DocumentCleaner().clean_document(document, english = True, return_list = True, stopwords = True)
        bow = self.id2word.doc2bow(cleaned_document)
        if self.trained_model:
            return self.trained_model[bow]
        return None


class NmfAgent(Model):


    def __init__(self, topn, documents=None):
        Model.__init__(self)
        self.topn = topn
        self.documents = documents
        self.preprocess(self.documents)


    def __get_nmf_topics(self, num_topics):
        #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
        model = NMF(n_components=num_topics, init='nndsvd')
        model.fit(self.xtfidf_norm)
        self.trained_model = model
        return self.extract_topics_from_trained_model(num_topics)
    

    def extract_topics_from_trained_model(self, num_topics):
        if self.trained_model:
            feat_names = self.vectorizer.get_feature_names()
            word_dict = {}
            for i in range(num_topics):
                #for each topic, obtain the largest values, and add the words they map to into the dictionary.
                words_ids = self.trained_model.components_[i].argsort()[:-self.topn - 1:-1]
                words = [feat_names[key] for key in words_ids]
                word_dict['Topic # ' + '{:02d}'.format(i+1)] = words
            return pd.DataFrame(word_dict)
        return None


    def preprocess(self, documents):
        if documents:
            self.cleaned_documents = [DocumentCleaner().clean_document(document, english = True, return_list = False, stopwords = True) for document in self.documents]
            self.vectorizer = CountVectorizer(analyzer='word', stop_words='english', lowercase=True, token_pattern=r'[^\d\W]{2,}')
            self.x_counts = self.vectorizer.fit_transform(self.cleaned_documents)
            self.words = self.vectorizer.get_feature_names()
            self.transformer = TfidfTransformer(smooth_idf=False)
            self.x_tfidf = self.transformer.fit_transform(self.x_counts)
            self.xtfidf_norm = normalize(self.x_tfidf, norm='l1', axis=1)


    def train(self, num_topics, use_tfidf=False):
        results = self.__get_nmf_topics(num_topics)
        self.last_trained_results = results
        return results


    def transform_unseen_document(self, document):
        cleaned_document = DocumentCleaner().clean_document(document, english = True, return_list = False, stopwords = True)
        return self.trained_model.transform(self.vectorizer.transform([cleaned_document]))[0]


class HdaAgent(Model):


    def train(self, num_topics):
        pass



