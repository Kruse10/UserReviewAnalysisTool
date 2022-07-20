import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class MainController:
    
    def __init__(self, model):
        self.model = model
        self.response = None
        
    def set_view(self, v):
        self.view = v

    def request_search(self):
        return InitialSearch(self.model)
        
    
 
        
class InitialSearch:
    def __init__(self, model):
        self.model = model

    target = 'https://www.imdb.com/title'

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
            #need to prompt user through view if there are 
            #still multiple links at this point
        
        if len(self.links)>1:
            _selecttitle = SelectTitle()
            links = _selecttitle.get_title(links)
            _selecttitle = None
            #self.links = self.view.select_link(self.links) #incorrect, url not obvious to human reader need to get title
                          #controller should wait for event signifying that the button in the link selection window has been pressed
                         #select link should return a message for a specific link or to keep some subset of self.links
        
        for url in self.links[:]:
            #grab and store data
            self.model.scraper.scrape_reviews(url)
           
        return self.links 
        #return links is incorrect and will be changed
        #need to send the links to the model to then scrape the target site and then return just the
        #title info, dataset size, and list of fields needed by the view


class SelectTitle:

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

class CheckColumns: 
    def check_columns(self):
            if (model.load_dataset(path)== "column check"):

                view.colWindow(model.df_temp.columns.values.toList()
                               , model.df_temp.loc[0].values.flatten().tolist())
            else:
                model.append_list()
                
