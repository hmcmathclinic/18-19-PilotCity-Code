import wikipedia
import pickle
import warnings
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
warnings.filterwarnings("ignore")


def create_layout(logo, story, styles):  
	im = Image(logo, 2*inch, 2*inch)
	Story.append(im)
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

	# Title
	ptext = '<b><font size=25>Study Guide</font></b>'
	Story.append(Paragraph(ptext, styles["Normal"]))         
	Story.append(Spacer(1, 20))


def get_topics():
	index_dict = "package/20topics_nmf_laspositas.sav"

	with open(index_dict, 'rb') as filehandle:
		indices = pickle.load(filehandle)
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

def add_data_to_document(Story, doc, styles):
	topics = get_topics()
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



doc = SimpleDocTemplate("study_guide.pdf",pagesize=letter,
	                        rightMargin=72,leftMargin=72,
	                        topMargin=72,bottomMargin=18)
Story=[]
logo = "logo.png"
styles=getSampleStyleSheet()

create_layout(logo,Story,styles)
add_data_to_document(Story, doc,styles)