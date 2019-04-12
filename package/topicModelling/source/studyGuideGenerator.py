import wikipedia
import pickle
import warnings
import sys
from learningAgents import LdaAgent,NmfAgent
from pdftextExtractor import PDFTextExtractor
from model import Model
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
warnings.filterwarnings("ignore")

class StudyGuideGenerator:

    def __init__(self, agent_fname, out_fname = "studyGuide_youJustMade.pdf"):
        ''' Initializes StudyGuideGenerator object with:
          -- the trained agent, given by agent_fname 
             (filepath/filename of trained learningAgents object)
          -- an empty document which will become the study guide
          -- an empty story (list of words to put in document)
          -- default styles for the document to have
        Note: supply your own study guide file name as the argument 
              "out_fname" if you'd like a particular name to be used
        '''
        self.agent = Model.load_saved_info(agent_fname)
        self.doc = SimpleDocTemplate(out_fname, pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
        self.story = [] 
        self.styles = getSampleStyleSheet()

    def create_layout(self, logo):  
        ''' Generates the layout for a standard study guide, 
        given a logo image to put in the document''' 
        im = Image(logo, 2*inch, 2*inch)
        self.story.append(im)
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        # Title
        ptext = '<b><font size=25>Study Guide</font></b>'
        self.story.append(Paragraph(ptext, self.styles["Normal"]))         
        self.story.append(Spacer(1, 20))

    def get_all_topics(self):
        ''' Retrieve all topics from the trained self.agent''' 
        indices = self.agent.get_last_trained_results()
        indices.values.T.tolist()
        return [list(l) for l in zip(*indices.values)]
    
    def get_topics_new_input(self, syllabus):
        ''' Retrieves the most relevant topics obtained by
        sending the trained agent an unseen syllabus '''
        extractor = PDFTextExtractor()
        # convert syllabus to string
        syllabus = extractor.convert_pdf_to_text(syllabus)
        indices = self.agent.transform_unseen_document(syllabus)
        indices.values.T.tolist()
        return [list(l) for l in zip(*indices.values)]

    def get_definition(self, topic):
        ''' Scrape Wikipedia to get a summary/definition of a topic'''
        try:
            results = wikipedia.search(topic)
            page = results[0]
            summary = wikipedia.summary(page, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            return -1
        return summary
    
    def add_data_to_document(self, topics):
        ''' Given a list of topics, scrape the Wikipedia 
        definition to add data to the document for each topic. '''
        for topic in topics:
            s = ''
            n = 0
            for word in topic:
                summary = self.get_definition(word)
                if summary != -1:
                    n += 1
                    s = "<b>" + word + "</b>" + ": " + summary
                    self.story.append(Spacer(1, 6))
                    self.story.append(Paragraph(s, self.styles["Justify"]))
                if n == 3:
                    break
            self.story.append(Spacer(1, 12))

        self.doc.build(self.story)

    def create_document(self, use_all_topics, image, syllabus = ""):
        ''' Generate a study guide! You have the option to either: 

            -- Generate a "study guide" of all the topics stored in 
               the trained self.agent by passing in "use_all_topics = True" 
               (useful if you don't have a particular syllabus you
               want to create a study guide for)

            -- Generate the study guide for a particular class's syllabus
               based on the top 5 most-represented topics from self.agent
               displayed in that syllabus (use_all_topics = False)'''
        if use_all_topics:
            topics = self.get_all_topics()
        else:
            if syllabus == "":
                print("If you don't want all the topics from the agent, \
                    please supply a syllabus name!")
            else:
                topics = self.get_topics_new_input(syllabus)
        self.create_layout(image)
        self.add_data_to_document(topics)
        