import csv
import re
import spacy
import sys
import requests
import pandas as pd
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
import os
import sys, getopt
import numpy as np
from bs4 import BeautifulSoup
import urllib3
from glob import glob
from string import punctuation
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def find_pdfs():
    return glob(os.path.join('./AllSyllabiParser',"*.{}".format('pdf')))

def convert(fname, pages=None):
    """ Function converting pdf to string """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(fname, 'rb')
    try:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
    except PDFTextExtractionNotAllowed:
        print('This pdf won\'t allow text extraction!')
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return strip_punctuation(text)
    
list_of_pdfs = find_pdfs()
common_texts = []
#Converting pdf to string
for pdf in list_of_pdfs:
    syllabus_string = convert(pdf)
    common_texts.append(syllabus_string.split())

common_dictionary = Dictionary(common_texts)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
lda = LdaModel(common_corpus, num_topics=10)