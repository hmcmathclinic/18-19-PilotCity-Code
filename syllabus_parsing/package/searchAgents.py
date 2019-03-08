import wikipedia


class SearchAgent:

    def search(self, keywords):
        pass


class WikipediaSearchAgent(SearchAgent):


    def search(self, keywords):
        search_phrase = " ".join(keywords)
        return wikipedia.search(search_phrase)