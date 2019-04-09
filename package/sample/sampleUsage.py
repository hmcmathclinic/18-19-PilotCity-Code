import sys
sys.path.append("../source")
from learningAgents import LdaAgent,NmfAgent
from pdftextExtractor import PDFTextExtractor
from model import Model
import pandas as pd

if __name__ == "__main__":
    '''
           #Create PDF Text Extractor, and supply path to folder contain relevant syllabus

        parser = PDFTextExtractor()
        documents = parser.get_documents_from_pdf_folder_path('path_To_PDFs')

            #Instantiate an LDA/NMF agent that uses LDA/NMF model to obtain topic distribution

        numberOfWordsPerTopics = 20
        numberOfTopics =  20
        agent = LdaAgent(documents)
        topics = agent.train(numberOfTopics, numberOfWordsPerTopics)
        print(topics)


            #Save Trained Agent
        agent.save_info(agent,"trained_agent-lda")

            #Load Trained Agent
        retrieved_agent = Model.load_saved_info("trained_agent-lda")

            #Visualize
        agent.visualize()

            #Get Topic Distribution for unseen document
        topics = agent.transform_unseen_document("computational complexity and algorithms make you a better computer scientist")
    '''
    parser = PDFTextExtractor()
    documents = parser.get_documents_from_pdf_folder_path('../AllSyllabiParser')
    numberOfWordsPerTopics = 20
    numberOfTopics =  20
    agent = NmfAgent(documents)
    topics = agent.train(numberOfTopics, numberOfWordsPerTopics)
    print(topics)
    print("Read SampleUsage.py for instructions")
    agent.visualize()