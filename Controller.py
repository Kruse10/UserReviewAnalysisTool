import requests
import urllib
from abc import ABC, abstractmethod
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class ab_Controller(ABC):
    @abstractmethod
    def __init__(self): pass


class MovieInfo:
    def __init__(self, url, t, y, d, k, c):
        self.url = url
        self.year = y
        self.director = d
        self.title = t
        self.keep = k

        
    def get_keep(self):
        return self.keep
    def get_str(self):
        return self.url + "\n" + self.year + " " + self.director

class MainController(ab_Controller):
    
    def __init__(self, model):
        self.model = model
        self.response = None
        self.waiting = False
    
    def set_view(self, v):
        self.view = v

    def request_search(self, query):
        return InitialSearch().get_search(query)
    
    def get_adv_search(self, q1, q2, q3, q4):
        return InitialSearch().get_adv_search(q1, q2, q3, q4)

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
 
        
class InitialSearch(ab_Controller):
    def __init__(self):
        self.target ='https://www.imdb.com/title'
        self.hd = { 'Accept-Language' : 'en-US,en;q=0.5' , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        self.session = HTMLSession()
        self.session.headers.update(self.hd)
    def getResponse(self, query):
        
        try:
            response = self.session.get(query)
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

    def filter_by(self, url, q1, dir, y1, q4):
        session = HTMLSession()
        hd = { 'Accept-Language' : 'en-US,en;q=0.5' , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        session.headers.update(hd)
        n_response = requests.get(url)
        page = BeautifulSoup(n_response.content, 'html.parser')
        k_year ='keep'
        k_dir = 'keep'
        y = str(page.find_all('span', class_='nobr'))
        n = 0
        nstring= ''
        for c in y:
            if n > 1 or c == r'/':
                break
            if c == '>':
                n+=1
            if n==1 and c!='>' and c!='<':
                nstring = nstring+c
        
        year = nstring.strip().strip(')').strip('(')
        if(y1 == ''):
            k_year = 'ignore'
        
        nstring = ''
        n=0
        d = str(page.find('td', class_="name"))
        for c in d:
            if n > 2:
                break
            if c == '>':
                n+=1
            if n==2 and c!='>' and c!='<':
                if c == r'/':
                    break
                else:
                    nstring= nstring+c        
        d=nstring.strip()
        n=0
        if(dir == ''):
            k_d = 'ignore'
        
        castlist= []
        cast = page.find_all('td', class_='primary_photo')
    
    
        for person in cast:
            castlist.append(person)
        
            n=0
            np=0
            nstring = ''
            for char in str(person):
            
                if np==2:
                    break
                if char == '>':
                    n+=1
                if n==2:
                    if char == '"':
                        np+=1
                    if np==1 and char != '"':
                        nstring=nstring+char
                    if np == 2:
                        break
            
            castlist.append(nstring)
        
        if ((k_year == 'ignore') and ( k_d == 'ignore')):
            return MovieInfo(url, q1,year,d, 'keep', castlist)
        elif ((k_year == 'ignore') and ( d == dir)) :
            return MovieInfo(url, q1,year,d, 'keep')
        elif ((year == y1) and (k_d == 'ignore')):
            return MovieInfo(url, q1,year,d, 'keep')
    
        if ((year != y1) or (d != dir)):
            return MovieInfo(url, q1, year, d, 'remove')
        else:
            return MovieInfo(url, q1,year,d, 'keep')



    def get_adv_search(self, q1, q2, q3, q4):
        q1 = ("https://www.google.com/search?q=" + "imdb" + q1)
        self.response = self.getResponse(q1)
        self.links = list(self.response.html.absolute_links)
        
        removed_endings = ["reviews", "critic", "trivia/", "external", "parentalguide"]
        for url in self.links[:]:
            remove = False
            if not (url.startswith(self.target)) or not(url.endswith('fullcredits')):
                remove = True
            for endstr in removed_endings:
                if url.endswith(endstr):
                    remove = True
            if remove == True:
                self.links.remove(url)
        self.movielist = []
        for url in self.links[:]:
            thismovie = self.filter_by(url, q1, q2, q3, q4)
            if (thismovie.get_keep() != 'keep'):
                self.links.remove(url)
            else:
                self.movielist.append(thismovie)
        for movie in self.movielist[:]:
            movie.url= movie.url[:len(url)-11]
            movie.url= movie.url+'reviews'
        return self.movielist


    

class GetTitles(ab_Controller):
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

class CheckColumns(ab_Controller):
    def __init__(self, v):
        self.view = v
    
    def check_columns(self, titles, row1):
        self.view.ColWindow(self, titles, row1)
        pass
                
