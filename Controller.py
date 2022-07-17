import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

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


