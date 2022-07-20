import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

class MainController:
    

    def __init__(self, model):
        self.model = model
        self.response = None
        self.target = 'https://www.imdb.com/title'

    def set_view(self, v):
        self.view = v
    def getResponse(self, query):
        
        try:
            session = HTMLSession()
            response = session.get(query)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            
    def get_search(self, query):
        query = urllib.parse.quote_plus(query)
        self.response = self.getResponse("https://www.google.com/search?q=" + "imdb" 
                              + query + "reviews")
        self.links = list(self.response.html.absolute_links)


        for url in self.links[:]:
            if not (url.startswith(self.target)) or "reviews" not in url or "critic" in url or "external" in url:
                self.links.remove(url)
            #need to prompt user through view if there are 
            #still multiple links at this point
        
        if len(self.links)>1:
            pass
            #self.links = self.view.select_link(self.links) #incorrect, url not obvious to human reader need to get title
                          #controller should wait for event signifying that the button in the link selection window has been pressed
                         #select link should return a message for a specific link or to keep some subset of self.links
        
        for url in self.links[:]:
            #self.model.get_response()    
            pass
        return self.links 
        #return links is incorrect and will be changed
        #need to send the links to the model to then scrape the target site and then return just the
        #title info, dataset size, and list of fields needed by the view
        


