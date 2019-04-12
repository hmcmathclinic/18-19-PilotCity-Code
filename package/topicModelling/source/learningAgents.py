from model import Model
from documentCleaner import DocumentCleaner
import gensim
import pandas as pd
from pdftextExtractor import PDFTextExtractor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE
import trainTopicModels
import pyLDAvis
import pyLDAvis.gensim
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import seaborn as sns

class LdaAgent(Model):


    def __init__(self, documents=None):
        Model.__init__(self)
        if not documents:
            raise ValueError("Pass a non-empy list of documents")
        self.documents = documents        
        self.preprocess(self.documents)


    def __get_lda_topics(self, num_topics, number_words_per_topic, use_tfidf):
        if not use_tfidf:
            model = gensim.models.ldamodel.LdaModel(self.bag_of_words_per_document, num_topics, id2word=self.id2word, passes=50)
        else:
            tfidf = gensim.models.TfidfModel(self.bag_of_words_per_document)
            corpus_tfidf = tfidf[self.bag_of_words_per_document]
            model = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics, id2word=self.id2word, passes=10)
        self.trained_model = model
        return self.extract_topics_from_trained_model(num_topics, number_words_per_topic)


    def extract_topics_from_trained_model(self, num_topics, number_words_per_topic):
        if self.trained_model:
            word_dict = {}
            for i in range(num_topics):
                words = self.trained_model.show_topic(i, topn = number_words_per_topic)
                word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words]
            return pd.DataFrame(word_dict)
        return None


    def preprocess(self, documents):
        if documents:
            self.cleaned_documents = [DocumentCleaner().clean_document(document, english = True, return_list = True, stopwords = True) 
                                    for document in self.documents]
            self.id2word = gensim.corpora.Dictionary(self.cleaned_documents)
            self.bag_of_words_per_document = [self.id2word.doc2bow(document) for document in self.cleaned_documents]


    def construct_model(self):
       trainTopicModels.trainModel(self,"LDA")


    def train(self, num_topics, number_words_per_topic=20, use_tfidf=False):
        results = self.__get_lda_topics(num_topics, number_words_per_topic, use_tfidf)
        self.last_trained_results = results
        return results


    def transform_unseen_document(self, document):
        cleaned_document = DocumentCleaner().clean_document(document, english = True, return_list = True, stopwords = True)
        bow = self.id2word.doc2bow(cleaned_document)
        if self.trained_model:
            topics = self.trained_model[bow]
            out = {}
            for topic in topics:
                key = 'Topic # ' + '{:02d}'.format(topic[0]+1)
                out[key] = self.last_trained_results[key]
            return pd.DataFrame(out)
        return None
    

    def visualize(self):
        print("Visualization works for LDA works only if you're running our code in a Jupyter Notebook")
        if self.trained_model:
            vis_data =pyLDAvis.gensim.prepare(self.trained_model, self.bag_of_words_per_document, self.id2word)
            pyLDAvis.display(vis_data)


class NmfAgent(Model):


    def __init__(self, documents=None):
        Model.__init__(self)
        if not documents:
            raise ValueError("Pass a non-empy list of documents")
        self.documents = documents
        self.preprocess(self.documents)


    def __get_nmf_topics(self, num_topics, number_words_per_topic):
        #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
        self.num_topics = num_topics
        model = NMF(n_components=num_topics, init='nndsvd')
        model.fit(self.xtfidf_norm)
        self.nmf_embedding = model.transform(self.xtfidf_norm)
        self.nmf_embedding = (self.nmf_embedding - self.nmf_embedding.mean(axis=0))/self.nmf_embedding.std(axis=0)
        self.trained_model = model
        return self.extract_topics_from_trained_model(num_topics, number_words_per_topic)
    
    
    def __center(self, points, d = 2):
        if len(points) == 0: return None
        elif d==2:
            return (sum([x[0] for x in points])/len(points), sum([x[1] for x in points])/len(points))
        elif d==3:
            return (sum([x[0] for x in points])/len(points), sum([x[1] for x in points])/len(points), sum([x[2] for x in points])/len(points))


    def extract_topics_from_trained_model(self, num_topics, number_words_per_topic):
        if self.trained_model:
            feat_names = self.vectorizer.get_feature_names()
            word_dict = {}
            for i in range(num_topics):
                #for each topic, obtain the largest values, and add the words they map to into the dictionary.
                words_ids = self.trained_model.components_[i].argsort()[:-number_words_per_topic - 1:-1]
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


    def construct_model(self):
        print("Starting process of training model")
        trainTopicModels.trainModel(self,"NMF")


    def train(self, num_topics, number_words_per_topic=20, use_tfidf=False):
        results = self.__get_nmf_topics(num_topics, number_words_per_topic)
        self.last_trained_results = results
        return results


    def transform_unseen_document(self, document, num_topics=5):
        cleaned_document = DocumentCleaner().clean_document(document, english = True, return_list = False, stopwords = True)
        topics = self.trained_model.transform(self.vectorizer.transform([cleaned_document]))[0]
        topics_and_id = [(i, topics[i]) for i in range(len(topics))]
        top_n_topics = sorted(topics_and_id, key=lambda x: x[1], reverse=True)[:num_topics]
        out = {}
        for topic_tup in top_n_topics:
            if topic_tup[1] > 0:
                key = 'Topic # ' + '{:02d}'.format(topic_tup[0]+1)
                out[key] = self.last_trained_results[key]
        return pd.DataFrame(out)
    

    def visualize(self, words_per_cluster=3):
        if self.trained_model:
            tsne = TSNE(random_state=3211)
            tsne_embedding = tsne.fit_transform(self.nmf_embedding)
            tsne_embedding = pd.DataFrame(tsne_embedding,columns=['x','y'])
            tsne_embedding['hue'] = self.nmf_embedding.argmax(axis=1)
            tsne_groups = [[] for x in range(self.num_topics)] 
            for i in range(len(tsne_embedding)):
                tsne_groups[tsne_embedding['hue'][i]].append((tsne_embedding['x'][i],tsne_embedding['y'][i]))
            tsne_centers = [self.__center(points) for points in tsne_groups]

            topic_words = [None]*self.num_topics
            for i in range(self.num_topics):
                topic_words[i] = '\n '.join(self.last_trained_results.iloc[0:words_per_cluster, i])

            font = {'family' : 'normal', 'size': 9}
            matplotlib.rc('font', **font)
            plt.figure(figsize=(20, 20))
            data = tsne_embedding
            plt.scatter(data=data,x='x',y='y',s=6,c=data['hue'],cmap="gist_ncar")
            for i, words in enumerate(topic_words):
                plt.annotate(words, (tsne_centers[i][0], tsne_centers[i][1]))
            plt.show()


class HdaAgent(Model):


    def train(self, num_topics):
        pass



