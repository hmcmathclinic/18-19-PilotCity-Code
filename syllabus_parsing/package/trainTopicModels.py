import learningAgents
from model import Model
from documentCleaner import DocumentCleaner
import gensim
import pandas as pd
from pdftextExtractor import PDFTextExtractor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
import pickle

def trainModel(type, documents, use_tfidf=True):
    ''' Type is either LDA or NMF. Set tfidf to true or false (LDA only) '''
    if type == "LDA":
        agent = learningAgents.LdaAgent(topn=100, documents=documents)
    elif type == "NMF": 
        agent = learningAgents.NmfAgent(topn=100, documents=documents)
    else: 
        return "Error! type needs to be either LDA or NMF"
    if use_tfidf: 
        addin = "TFIDF"
    else:
        addin = ""
    for num_topics in range(1, 41, 1):
        print("Training " + type + " model on ", str(num_topics), " topics with" + addin)
        topics = agent.train(num_topics, use_tfidf)
        print(topics)
        name = str(num_topics) + "topics_" + type + addin + "_laspositas.sav"
        agent.save_info(topics, name)
        name = str(num_topics) + "topics_agent_" + type + addin + "_laspositas.sav"
        agent.save_info(agent, name)

if __name__ == "__main__":
    parser = PDFTextExtractor()
    #documents = parser.get_documents_from_pdf_folder_path('../AllSyllabiParser')
    
    # las positas syllabi
    documents = parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi2')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi3')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi4')

    trainModel(documents=documents, use_tfidf=True, type = "NMF")
