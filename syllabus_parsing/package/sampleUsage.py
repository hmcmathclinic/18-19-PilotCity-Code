from learningAgents import LdaAgent,NmfAgent
from pdftextExtractor import PDFTextExtractor
from model import Model
import pandas as pd

if __name__ == "__main__":
    #Create PDF Text Extractor, and supply path to folder contain relevant syllabus
    # parser = PDFTextExtractor()
    # documents = parser.get_documents_from_pdf_folder_path('../AllSyllabiParser')
    # #Instantiate an LDA agent that uses LDA model to obtain topic distribution
    # agent = LdaAgent(20, documents)
    # print(agent.train(20))
    # print(agent.transform_unseen_document("computational complexity is the best topic in computer science"))
    # # Save a trained agent
    # agent.save_info(agent, "trained_agent")
    ## Retrieve a saved agent
    # retrieved_agent = Model.load_saved_info("trained_agent")
    # results = retrieved_agent.get_last_trained_results()
    # topics = retrieved_agent.transform_unseen_document("computational complexity and algorithms make you a better computer scientist")
    # print(topics)

    # #Instantiate an LDA agent that uses LDA model to obtain topic distribution
    agent2 = Model.load_saved_info("trained-agent-nmf")
    topics2 = agent2.transform_unseen_document("computational complexity and algorithms make you a better computer scientist")
    print(topics2)


