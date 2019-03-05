import re
from nltk.corpus import words, stopwords


class DocumentCleaner:

    def __init__(self):
        self.allEnglishWords = set(words.words())
        self.stopwordsList = set(stopwords.words('english'))


    def clean_document(self,doc, english = False, return_list = False, stopwords = False):
        listOfWords = re.findall(r'[^\d\W]{2,}', doc)
        listOfWords = [word.lower() for word in listOfWords]
        if english:
            listOfWords = [word for word in listOfWords if word in self.allEnglishWords]
        if stopwords:
            listOfWords = [word for word in listOfWords if word not in self.stopwordsList]
        if return_list:
            return listOfWords
        else:
            return " ".join(listOfWords)

    


