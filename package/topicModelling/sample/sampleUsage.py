import sys
sys.path.append("../source")
from learningAgents import LdaAgent,NmfAgent
from pdftextExtractor import PDFTextExtractor
from studyGuideGenerator import StudyGuideGenerator
from model import Model
import pandas as pd
import config

outputPath = config.CONFIG["outputPath"]


if __name__ == "__main__":
    '''
           #Create PDF Text Extractor, and supply path to folder contain relevant syllabus

        parser = PDFTextExtractor()
        documents = parser.get_documents_from_pdf_folder_path('path_To_PDFs')

            #Instantiate an LDA/NMF agent that uses LDA/NMF model to obtain topic distribution

        agent = NmfAgent(documents)
        # or use agent = LdaAgent(documents)
        agent.construct_model()
        topics = agent.get_last_trained_results()
        print(topics)

            # Save Trained Agent
        agent.save_info(agent,"trained_agent-lda")

            # Load Trained Agent
        retrieved_agent = Model.load_saved_info("trained_agent-lda")

            # Visualize
        agent.visualize()

            # Get Topic Distribution for unseen document
        topics = agent.transform_unseen_document("computational complexity and algorithms make you a better computer scientist")
    
            # Generate a Study Guide
        # What trained agent do you want to use?
        trained_agent_filepath = outputPath + "/trained_agent-nmf"
        generator = StudyGuideGenerator(agent_fname=trained_agent_filepath)

        # For what syllabus do you want a study guide?
        syllabus = "../syllabi/LasPositasSyllabi1/course_outline_pdf - 2019-02-28T120643.112.pdf"

        # What image would you like to appear on the document?
        logo = "../images/logo.png"

        # Create the study guide
        generator.create_document(use_all_topics=False, image = logo, syllabus=syllabus)
    '''
    parser = PDFTextExtractor()
    documents = parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi1')
    # documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi2')
    # documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi3')
    # documents += parser.get_documents_from_pdf_folder_path('../syllabi/LasPositasSyllabi4')
    agent = NmfAgent(documents)
    agent.construct_model()
    topics = agent.get_last_trained_results()
    print(topics)
    agent.save_info(agent, outputPath + "/trained_agent-nmf")
    agent.visualize()

    # generate study guide
    # What trained agent do you want to use?
    trained_agent_filepath = outputPath + "/trained_agent-nmf"
    generator = StudyGuideGenerator(agent_fname=trained_agent_filepath)
    # For what syllabus do you want a study guide?
    syllabus = "../syllabi/LasPositasSyllabi1/course_outline_pdf - 2019-02-28T120643.112.pdf"
    # What image would you like to appear on the document?
    logo = "../images/logo.png"
    # Create the study guide
    generator.create_document(use_all_topics=False, image = logo, syllabus=syllabus)
