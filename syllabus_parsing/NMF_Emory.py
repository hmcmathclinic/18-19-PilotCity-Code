
# coding: utf-8

# In[1]:


import pandas as pd;
import numpy as np;
import scipy as sp;
import sklearn;
import sys;
from nltk.corpus import stopwords;
import nltk;
from gensim.models import ldamodel
import gensim.corpora;
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer;
from sklearn.decomposition import NMF;
from sklearn.preprocessing import normalize;
from sklearn.decomposition import TruncatedSVD
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim
import pickle;
#import utilities

#utils = utilities.Utils()



pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# In[2]:


from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import random 
random.seed(13)

#visualization packages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import seaborn as sns


# In[13]:


import csv
import re
#import spacy
import sys
import requests
import pandas as pd
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
import os
import sys, getopt
import numpy as np
from bs4 import BeautifulSoup
import urllib3
from glob import glob
from string import punctuation

from nltk.corpus import wordnet

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def find_pdfs():
    list_of_pdfs = []
    pdf_dict = {} # records the indices of the pdfs by year
    for x in range(1990, 2020):
        start = len(list_of_pdfs)
        list_of_pdfs += glob(os.path.join('./EmoryUniversitySyllabi/'+str(x),"*.{}".format('pdf')))
        pdf_dict[x] = list(range(start,len(list_of_pdfs)))
    return list_of_pdfs, pdf_dict

def convert(fname, pages=None):
    """ Function converting pdf to string """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    
    try:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
    except PDFTextExtractionNotAllowed:
        print('This pdf won\'t allow text extraction!')
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return strip_punctuation(text)

def word_count(string):
    my_string = string.lower().split()
    my_dict = {}
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
    


# In[25]:


list_of_pdfs, pdfs_by_year = find_pdfs()
syllabus_string = ''
bag_of_words_all_syllabi = []
corpus = []
#Converting pdf to string


# In[29]:


for pdf in list_of_pdfs[2803:]:
    syllabus_string = convert(pdf)
    corpus.append(syllabus_string)
#     bag_of_words_one_syllabus = word_count(syllabus_string)
#     bag_of_words_all_syllabi.append(bag_of_words_one_syllabus)


# In[27]:


len(corpus)


# In[22]:


len(list_of_pdfs)


# In[30]:


len(corpus)


# In[32]:


corpus = corpus[:2802] + [' '] + corpus[2802:]


# In[74]:


import copy
oldcorpus = copy.deepcopy(corpus)


# In[75]:


startindex = pdfs_by_year[2001][0]


# In[78]:


corpus = corpus[startindex:]


# **Text Cleaning**

# In[165]:


from nltk.corpus import words
from nltk.corpus import stopwords
import spacy

nlp = spacy.load('en_core_web_lg', disable=['parser', 'ner'])

allEnglishWords = set(words.words())
stopwordsList = set(stopwords.words('english'))

def clean_doc(doc, english = False, return_list = False, stopwords = False):
    listOfWords = re.findall(r'[^\d\W]{2,}', doc)
    listOfWords = [word.lower() for word in listOfWords if len(word) > 2 and word not in uselessWords]
    if english:
        listOfWords = [word for word in listOfWords if word in allEnglishWords]
    if stopwords:
        listOfWords = [word for word in listOfWords if word not in stopwordsList]
    if return_list:
        return listOfWords
    else:
        return " ".join(listOfWords)

def lemmatize(doc, return_list = False):
    doc = nlp(doc)
    if return_list:
        return [token.lemma_ for token in doc]
    else:
        return " ".join([token.lemma_ for token in doc])


# In[93]:


cleaned_corpus = [clean_doc(doc, return_list = True, stopwords = True) for doc in corpus]


# In[94]:


cleaned_corpus_1 = [clean_doc(doc, english = True, return_list = True, stopwords = True) for doc in corpus]


# In[95]:


cleaned_corpus_2 = [clean_doc(doc, english = True, return_list = False, stopwords = True) for doc in corpus]


# In[96]:


cleaned_corpus_3 = [clean_doc(doc, english = False, return_list = False, stopwords = True) for doc in corpus]


# In[97]:


cleaned_corpus_4 = [clean_doc(doc, english = False, return_list = True, stopwords = True) for doc in corpus]


# In[164]:


cleaned_lemma_corpus_NMF = [lemmatize(doc) for doc in cleaned_corpus_2]


# In[161]:


cleaned_lemma_corpus_NMF1 = [lemmatize(doc) for doc in cleaned_corpus_2]


# **NMF**

# In[98]:


vectorizer = CountVectorizer(analyzer='word', stop_words='english', lowercase=True, token_pattern=r'[^\d\W]{2,}', ngram_range = (1,1), max_df = 0.9);
x_counts = vectorizer.fit_transform(cleaned_corpus_2);


# In[99]:


transformer = TfidfTransformer(smooth_idf=True);
x_tfidf = transformer.fit_transform(x_counts);


# In[100]:


xtfidf_norm = normalize(x_tfidf, norm='l1', axis=1)


# In[101]:


def get_nmf_topics(model, num_topics, top_n_words):
    
    #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    feat_names = vectorizer.get_feature_names()
    
    word_dict = {};
    for i in range(num_topics):
        
        #for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-top_n_words - 1:-1]
        words = [feat_names[key] for key in words_ids]
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = words;
    
    return pd.DataFrame(word_dict);


# In[138]:


num_topics = 100
nmf_model = NMF(n_components=num_topics, init='nndsvd', shuffle = True)
nmf_model.fit(xtfidf_norm)
nmf_embedding = nmf_model.transform(xtfidf_norm)
nmf_embedding = (nmf_embedding - nmf_embedding.mean(axis=0))/nmf_embedding.std(axis=0)


# In[137]:


get_nmf_topics(nmf_model, num_topics,10)


# In[136]:


nmf_model.reconstruction_err_


# In[139]:


get_nmf_topics(nmf_model, num_topics,10)


# In[162]:


uselessWords = ['canvas, homework', 'use', 'semester', 'work', 'test', 'exam', 'project', 'quiz', 'unit', 'week','assignment',                'lecture', 'reading', 'student', 'mon', 'tue', 'wed', 'thur', 'fri', 'paper', 'examen']


# In[141]:


transformed = nmf_model.transform(xtfidf_norm)


# In[147]:


docTopTopics = np.argmax(transformed, axis = 1)


# In[149]:


import matplotlib.pyplot as plt


# In[155]:


numPerTopic, _ = np.histogram(docTopTopics, bins = 100)
sum(numPerTopic)


# In[152]:


plt.hist(docTopTopics, bins = 100)


# **Visualize using T-SNE**

# In[535]:


tsne = TSNE(random_state=3211)
tsne_embedding = tsne.fit_transform(nmf_embedding)
tsne_embedding = pd.DataFrame(tsne_embedding,columns=['x','y'])
tsne_embedding['hue'] = nmf_embedding.argmax(axis=1)


# In[536]:


def center(points, d = 2):
    if len(points) == 0: return None
    elif d==2:
        return (sum([x[0] for x in points])/len(points), sum([x[1] for x in points])/len(points))
    elif d==3:
        return (sum([x[0] for x in points])/len(points), sum([x[1] for x in points])/len(points), sum([x[2] for x in points])/len(points))


# In[537]:


tsne_groups = [[] for x in range(num_topics)] 
for i in range(len(tsne_embedding)):
    tsne_groups[tsne_embedding['hue'][i]].append((tsne_embedding['x'][i],tsne_embedding['y'][i]))
tsne_centers = [center(points) for points in tsne_groups]


# In[541]:


def top_n_words(n):
    topic_words = [None]*num_topics
    wordsDf = get_nmf_topics(nmf_model, num_topics,n)
    for i in range(num_topics):
        topic_words[i] = '\n '.join(wordsDf.iloc[0:n, i])
    return topic_words

topic_words = top_n_words(3)
topic_words


# In[545]:


font = {'family' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)


# In[546]:


fig = plt.figure(figsize=(20, 20))
data = tsne_embedding
scatter = plt.scatter(data=data,x='x',y='y',s=6,c=data['hue'],cmap="gist_ncar")
for i, words in enumerate(topic_words):
    plt.annotate(words, (tsne_centers[i][0], tsne_centers[i][1]))
plt.show()
plt.savefig("nmf_25.png")


# In[245]:


# fig = plt.figure(figsize=(20, 20))
# data = tsne_embedding
# scatter = plt.scatter(data=data,x='x',y='y',s=6,c=data['hue'],cmap="gist_ncar")
# for i, words in enumerate(topic_words):
#     plt.annotate(words, (tsne_centers[i][0], tsne_centers[i][1]))
# plt.show()


# In[389]:


tsne = TSNE(n_components=3, random_state=3211)
tsne_embedding = tsne.fit_transform(nmf_embedding)
tsne_embedding = pd.DataFrame(tsne_embedding,columns=['x','y','z'])
tsne_embedding['hue'] = nmf_embedding.argmax(axis=1)


# In[390]:


tsne_groups = [[] for x in range(num_topics)] 
for i in range(len(tsne_embedding)):
    tsne_groups[tsne_embedding['hue'][i]].append((tsne_embedding['x'][i],tsne_embedding['y'][i],tsne_embedding['z'][i]))
tsne_centers = [center(points, d=3) for points in tsne_groups]
topic_numbers = list(range(num_topics))


# In[391]:


from mpl_toolkits import mplot3d
get_ipython().run_line_magic('matplotlib', 'notebook')


fig3d = plt.figure('3d', figsize = (20, 20))
ax = plt.axes(projection='3d')

ax.scatter3D(tsne_embedding['x'], tsne_embedding['y'], tsne_embedding['z'],s=15, c=tsne_embedding['hue'], cmap='gist_ncar')
for i, num in enumerate(topic_numbers):
    ax.text(tsne_centers[i][0], tsne_centers[i][1], tsne_centers[i][2], num)


# **Checking Topic Coherence Visually using Glove**

# In[339]:


def get_vec(word):
    return utils.get_vec(word, utils.wordL, utils.array, utils.lengths)


# In[392]:


word_embedding = np.array([get_vec(word)[0] for word in top_n_words(1)])

tsne_word_embedding = tsne.fit_transform(word_embedding)
tsne_word_embedding = pd.DataFrame(tsne_word_embedding,columns=['x','y'])


# In[ ]:


tsne_word_embedding


# In[375]:


from sklearn.decomposition import PCA

data = pd.DataFrame(PCA(n_components = 2).fit_transform(word_embedding),columns=['x','y'])


# In[ ]:


# using first word to represent topic


fig = plt.figure(figsize=(15, 15))
data = tsne_word_embedding
topic_words = top_n_words(1)
scatter = plt.scatter(data=data,x='x',y='y',s=6,cmap="gist_ncar")
for i, words in enumerate(topic_words):
    plt.annotate(words, (data.values[i][0], data.values[i][1]))
plt.show()


# **Reducing Dimension using SVD**

# In[196]:


svd = TruncatedSVD(n_components=2, n_iter=7, random_state=42)
svd_embedding = svd.fit_transform(nmf_embedding)
svd_embedding = pd.DataFrame(svd_embedding,columns=['x','y'])
svd_embedding['hue'] = nmf_embedding.argmax(axis=1)


# In[197]:


fig2 = plt.figure(figsize=(20, 20))
data = svd_embedding
scatter = plt.scatter(data=data,x='x',y='y',s=6,c=data['hue'],cmap="Set1")


# **LDA**

# In[104]:


corpus_used = cleaned_corpus_1


# In[105]:


id2word = gensim.corpora.Dictionary(corpus_used);
id2word


# In[106]:


bow_corpus = [id2word.doc2bow(doc) for doc in corpus_used]


# In[107]:


tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]


# In[108]:


num_topics = 100


# In[114]:


lda = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics=num_topics, id2word=id2word, passes=15, random_state = 42)


# In[120]:


lda_tfidf = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=id2word, passes=100, random_state = 42)


# In[116]:


def get_lda_topics(model, num_topics):
    word_dict = {};
    for i in range(num_topics):
        words = model.show_topic(i, topn = 20);
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words];
    return pd.DataFrame(word_dict);


# In[121]:


get_lda_topics(lda_tfidf, num_topics)


# In[525]:


vis_data =pyLDAvis.gensim.prepare(lda, bow_corpus, id2word)
pyLDAvis.display(vis_data)


# **Determine the optimal number of topics**

# In[435]:


from itertools import combinations


# In[436]:


def calculate_coherence(topics_df, top = 5):
    skipped_over = 0
    num_topics = topics_df.shape[1]
    print(num_topics)
    topics_df = topics_df.head(top) # how many words do we actually want to look at?
    overall_coherence = 0.0
    for column in topics_df:
        # check each pair of terms
        pair_scores = []
        for pair in combinations(topics_df[column], 2 ):
            if not pair[0] in utils.wordL or not pair[1] in utils.wordL:
                skipped_over += 1
                continue   # skip if not there 
            score = utils.score(pair[0], pair[1]) 
            pair_scores.append(score)
            if score > 1 or score < -1: 
                print("problem!")
                print(score)
        # get the mean for all pairs in this topic
        topic_score = sum(pair_scores) / len(pair_scores)
        overall_coherence += topic_score
    # get the mean score across all topics
    return overall_coherence / num_topics, skipped_over


# In[438]:


calculate_coherence(get_lda_topics(lda_tfidf, num_topics), 3)


# In[439]:


topic_coh = []


# In[502]:


for i in range(10, 80):
    lda_tfidf = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=i, id2word=id2word, passes=5, random_state = 42)
    cohs = calculate_coherence(get_lda_topics(lda_tfidf, i), 3)[0]
    print(cohs)
    topic_coh.append(cohs)


# In[493]:


topic_coh3 = []
for i in range(10, 80):
    lda_tfidf = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics=i, id2word=id2word, passes=5, random_state = 42)
    coh = calculate_coherence(get_lda_topics(lda_tfidf, i), 3)[0]
    print(coh)
    topic_coh3.append(coh)


# In[ ]:


topic_coh


# In[518]:


plt.figure(0)
plt.title('bow')
plt.xlabel('num_topics')
plt.ylabel('topic coherence')
plt.plot(list(range(10,80)), topic_coh3)
plt.savefig('LDA_bow_coherence')


# In[507]:


len(topic_coh[30:100])


# In[498]:


len(topic_coh)


# In[516]:


plt.figure()
plt.title('TFIDF')
plt.xlabel('num_topics')
plt.ylabel('topic coherence')
plt.plot(list(range(10,80)), topic_coh[30:100])
plt.savefig('LDA_tfidf_coherence')


# **HDP**

# In[113]:


from gensim.models import HdpModel


# In[114]:


def get_hdp_topics(model, num_topics):
    word_dict = {};
    for i in range(num_topics):
        words = model.show_topic(i, topn = 20);
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words];
    return pd.DataFrame(word_dict);


# In[115]:


hdp = gensim.models.hdpmodel.HdpModel(bow_corpus, id2word=id2word)


# In[116]:


hdp_tfidf = gensim.models.hdpmodel.HdpModel(corpus_tfidf, id2word=id2word)


# In[72]:


get_hdp_topics(hdp, 10)


# In[118]:


get_hdp_topics(hdp_tfidf, 15)


# Hierarchical Dirichlet Process doesn't seem to work very well 
