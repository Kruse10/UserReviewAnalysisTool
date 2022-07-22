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
        self.waiting = False
    def set_view(self, v):
        self.view = v

    def request_search(self, query):
        return InitialSearch().get_search(query)
    
    def get_adv_search(self, q1, q2, q3):
        return InitialSearch().get_adv_search(q1, q2, q3)

    def gather_data(self, l):
        for item in l:
            if l[item].startswith("http"):
                self.model.build_df(l[item], "url")
            else:
                returnstr = self.model.build_df(list[item], "path")
                if isinstance(returntype, list):
                    CheckColumns(self.view).check_columns(model.d.new_df.columns , model.d.new_df.iloc[0])
                    
        self.model.build_report()        
        return self.model.visualize_data(vistype)            
    def gather_data(self, l, collist):
        pass
 
        
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
        query = ("https://www.google.com/search?q=" + "imdb" 
                              + query + "reviews")
        self.response = self.getResponse(query)
        self.links = list(self.response.html.absolute_links)

        for url in self.links[:]:
            if not (url.startswith(self.target)) or "reviews" not in url or "critic" in url or "external" in url:
                self.links.remove(url)
                          
        return self.links

    def get_adv_search(self, q1, q2, q3):
        q1 = ("https://www.google.com/search?q=" + "imdb" + q1)
        self.response = self.getResponse(q1)
        self.links = list(self.response.html.absolute_links)
        
        removed_endings = ["reviews", "critic", "trivia/", "external", "parentalguide", "fullcredits"]
        for url in self.links[:]:
            if not (url.startswith(self.target)):
                self.links.remove(url)
            for endstr in removed_endings:
                if url.endswith(endstr):
                    self.links.remove(url)
        
        filter_by(q2, q3)

        return self.links


    def filter_by(q2, q3):
        #search the pages and remove results that dont match criteria
        pass

class SelectTitle(Controller):
    #unfinished
    def get_title(self, links):
        initialsearch = InitialSearch()
        titles = List()
        for url in links:
            response = initialsearch.getResponse(url)
            page = BeautifulSoup(self.response.content, 'html.parser')
            #following line is almost certainly incomplete from what I remember
            pass
            titles.append(moviename)
        return titles

class CheckColumns(Controller):
    def __init__(self, v):
        self.view = v
    
    def check_columns(self, titles, row1):
        self.view.ColWindow(self, titles, row1)
        pass
                
