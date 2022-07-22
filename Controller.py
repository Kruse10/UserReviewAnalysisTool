import requests
import urllib
from abc import ABC, abstractmethod
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class Controller(ABC):
    @abstractmethod
    def __init__(self): pass




class MainController(Controller):
    
    def __init__(self, model):
        self.model = model
        self.response = None
        
    def set_view(self, v):
        self.view = v

    def request_search(self, query):
        return InitialSearch().get_search(query)


    def analyze_data(self, list):
        for item in list:
            if list[item].startswith("http"):
                self.model.scraper.scrape_reviews(list[item])
            else:
                self.model.load_dataset(list[item])
                
    
 
        
class InitialSearch(Controller):
    def __init__(self):
        self.target ='https://www.imdb.com/title'
    def getResponse(self, query):
        
        try:
            session = HTMLSession()
            response = session.get(query)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

         
    def get_search(self, query):
        query = urllib.parse.quote_plus(query)
        query = ("https://www.google.com/search?q=" + "imdb" 
                              + query + "reviews")
        self.response = self.getResponse(query)
        self.links = list(self.response.html.absolute_links)

        for url in self.links[:]:
            if not (url.startswith(self.target)) or "reviews" not in url or "critic" in url or "external" in url:
                self.links.remove(url)
                          
        return self.links 


class SelectTitle(Controller):

    def get_title(self, links):
        initialsearch = InitialSearch()
        titles = List()
        for url in links:
            response = initialsearch.getResponse(url)
            page = BeautifulSoup(self.response.content, 'html.parser')
            #following line is almost certainly incomplete from what I remember
            moviename = page.find('div', class_="parent").get_text()
            titles.append(moviename)
        return titles

class CheckColumns(Controller): 
    def check_columns(self):
            if (model.load_dataset(path)== "column check"):

                view.colWindow(model.df_temp.columns.values.toList()
                               , model.df_temp.loc[0].values.flatten().tolist())
            else:
                model.append_list()
                
