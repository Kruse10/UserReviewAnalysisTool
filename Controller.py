import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

class MainController:
    def __init__(self, model):
        self.model = model
    def set_view(self, v):
        self.view = v
    def getResponse(query):
        try:
            session = HTMLSession()
            response = session.get(query)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            
    def get_search(self, query):
        query = urllib.parse.quote_plus(query)
        response = getResponse("https://www.google.com/search?q="
                              + query + "reviews")
        links = list(response.html.absolute_links)

        target = 'http://www.imdb.com/title'

        for url in links[:]:
            if not (url.startswith(target)) or "reviews" not in url:
                links.remove(url)
            #need to prompt user through view if there are 
            #still multiple links at this point

        return links 
        #return links is incorrect and will be changed
        #need to send the links to the model to then scrape the target site and then return just the
        #title info, dataset size, and list of fields needed by the view
        


