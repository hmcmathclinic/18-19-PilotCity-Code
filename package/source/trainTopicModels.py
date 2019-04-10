from itertools import combinations
import learningAgents
import utilities
from model import Model
from documentCleaner import DocumentCleaner
import gensim
import pandas as pd
from pdftextExtractor import PDFTextExtractor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
import pickle

utils = utilities.Utils()

def trainModel(type, documents, use_tfidf=True):
    ''' Type is either LDA or NMF. Set tfidf to true or false (LDA only) '''
    if type == "LDA":
        agent = learningAgents.LdaAgent(documents=documents)
    elif type == "NMF": 
        agent = learningAgents.NmfAgent(documents=documents)
    else: 
        return "Error! type needs to be either LDA or NMF"
    if use_tfidf: 
        addin = "TFIDF"
    else:
        addin = ""
    topic_coherence = []
    for num_topics in range(10, 20, 1):
        print("Training " + type + " model on ", str(num_topics), " topics with" + addin)
        topics = agent.train(num_topics, use_tfidf=use_tfidf)
        score = calculate_coherence(topics)
        topic_coherence.append(score)
    ymax = max(topic_coherence)
    num_topics = topic_coherence.index(ymax) + 10
    topics = agent.train(num_topics, use_tfidf)
    name = str(num_topics) + "topics_" + type + addin + "_laspositas.sav"
    agent.save_info(topics, name)
    return topics

def calculate_coherence(topics_df, top = 3):
    skipped_over = 0
    num_topics = topics_df.shape[1]
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

if __name__ == "__main__":
    parser = PDFTextExtractor()
    #documents = parser.get_documents_from_pdf_folder_path('../AllSyllabiParser')
    print("Parser initialized")
    # las positas syllabi
    documents = parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi1')
    documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi2')
    documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi3')
    documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi4')
    trainModel(documents=documents, use_tfidf=True, type = "NMF")
    trainModel(documents=documents, use_tfidf=True, type = "LDA")
