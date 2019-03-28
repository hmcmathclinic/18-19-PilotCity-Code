from learningAgents import LdaAgent,NmfAgent
from pdftextExtractor import PDFTextExtractor
from model import Model

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
    #retrieved_agent = Model.load_saved_info("trained_agent")
    # print(retrieved_agent.get_last_trained_results())
    # print(retrieved_agent.transform_unseen_document("computational complexity is the best topic in computer science"))

    retrieved_agent = Model.load_saved_info("../trained_models/NMF_1_40_1/16topics_agent_NMFTFIDF_laspositas.sav")
    print(retrieved_agent.get_last_trained_results())
    print(retrieved_agent.transform_unseen_document("computational complexity is the best topic in computer science"))