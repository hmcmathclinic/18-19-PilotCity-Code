from glob import glob
import os
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
from string import punctuation


class PDFTextExtractor:


    def __init__(self):
        pass


    def find_pdfs(self, folder_path):
        return glob(os.path.join('{}'.format(folder_path),"*.{}".format('pdf')))
    

    def convert_pdf_to_text(self, fname, pages=None):
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
        return self.__strip_punctuation(text)

    
    def build_corpus_from_pdf_folder_path(self, folder_path):
        corpus = []
        list_of_pdfs = self.find_pdfs(folder_path)
        for pdf in list_of_pdfs:
            syllabus_string = self.convert_pdf_to_text(pdf)
            corpus.append(syllabus_string)
        return corpus

    
    def __strip_punctuation(self, s):
        return ''.join(c for c in s if c not in punctuation)


## Test
# if __name__ == "__main__":
#     parser = PDFTextExtractor()
#     print(parser.convert_pdf_to_text('../AllSyllabiParser/math2010.pdf'))
#     print(parser.find_pdfs('../AllSyllabiParser'))
     
