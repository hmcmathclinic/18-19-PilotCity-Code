import learningAgents

if __name__ == "__main__":
    parser = PDFTextExtractor()
    #documents = parser.get_documents_from_pdf_folder_path('../AllSyllabiParser')
    
    # las positas syllabi
    documents = parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi2')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi3')
    documents += parser.get_documents_from_pdf_folder_path('../LosPositasSyllabi4')
    agent = NmfAgent(documents)
    topics = agent.train(50)
    print(topics)
    name = "50topics_nmf_laspositas.sav"
    with open(name, 'wb') as filehandle:
        pickle.dump(topics, filehandle)
    name = "nmf_model_50topics_laspositas.sav"
    with open(name, 'wb') as filehandle:
        pickle.dump(agent, filehandle)