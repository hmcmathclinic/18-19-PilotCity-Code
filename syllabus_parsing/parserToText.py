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
import os
import sys, getopt
import numpy as np
from bs4 import BeautifulSoup
import urllib3
from glob import glob
from string import punctuation

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def find_pdfs():
    return glob(os.path.join('./HMCSyllabusRepository',"*.{}".format('pdf')))

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
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return strip_punctuation(text)

def word_count(string):
    my_string = string.lower().split()
    my_dict = {}
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
    
list_of_pdfs = find_pdfs()
syllabus_string = ''
bag_of_words_all_syllabi = []
#Converting pdf to string
for pdf in list_of_pdfs:
    syllabus_string = convert(pdf)
    bag_of_words_one_syllabus = word_count(syllabus_string)
    bag_of_words_all_syllabi.append(bag_of_words_one_syllabus)