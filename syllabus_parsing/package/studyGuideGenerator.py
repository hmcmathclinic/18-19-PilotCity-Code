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

    def __init__(self, agent_fname):
        # the previously-generated LdaAgent or NmfAgent (trained topics model)
        self.agent = Model.load_saved_info(agent_fname)

    def create_layout(logo, story, styles):  
        ''' Generates the layout for a standard study guide ''' 
        im = Image(logo, 2*inch, 2*inch)
        Story.append(im)
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        # Title
        ptext = '<b><font size=25>Study Guide</font></b>'
        Story.append(Paragraph(ptext, styles["Normal"]))         
        Story.append(Spacer(1, 20))

    def get_all_topics(topics_fname):
        ''' Retrieve all topics from the trained self.agent''' 
        indices = agent.get_last_trained_results()
        indices.values.T.tolist()
        return [list(l) for l in zip(*indices.values)]
    
    def get_topics_new_input(syllabus):
        ''' Retrieves the most relevant topics obtained by
        sending the trained agent an unseen syllabus '''
        extractor = PDFTextExtractor()
        # convert syllabus to string
        syllabus = extractor.convert_pdf_to_text(syllabus)
        indices = self.agent.transform_unseen_document(syllabus)
        indices.values.T.tolist()
        return [list(l) for l in zip(*indices.values)]

    def get_definition(topic):
        try:
        results = wikipedia.search(topic)
        page = results[0]
        summary = wikipedia.summary(page, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            return -1
        return summary
    
    def add_data_to_document(Story, doc, styles, syllabus):
        topics = get_topics()
        #topics = get_topics_new_input(syllabus)
        for topic in topics:
            s = ''
            n = 0
            for word in topic:
                summary = get_definition(word)
                if summary != -1:
                    n += 1
                    s = "<b>" + word + "</b>" + ": " + summary
                    Story.append(Spacer(1, 6))
                    Story.append(Paragraph(s, styles["Justify"]))
                if n == 3:
                    break
            Story.append(Spacer(1, 12))

        doc.build(Story)

def main():
    # For what syllabus do you want a study guide?
    syllabus = "../LosPositasSyllabi/course_outline_pdf - 2019-02-28T120643.112.pdf"

    doc = SimpleDocTemplate("2019-02-28T120643.112_study_guide.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    logo = "logo.png"
    styles=getSampleStyleSheet()

    create_layout(logo,Story,styles)
    add_data_to_document(Story, doc, styles, syllabus )

