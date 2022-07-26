import requests
import urllib
from abc import ABC, abstractmethod
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup


class ab_Controller(ABC):
    @abstractmethod
    def __init__(self): pass


class ab_ProductType_Info(ABC):
    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def get_keep(self): pass

    @abstractmethod
    def get_str(self): pass

#holds basic movie info and how to output to view 
class MovieInfo(ab_ProductType_Info):
    def __init__(self, url, t, y, d, k, c):
        self.url = str(url)
        self.year = str(y)
        self.director = str(d)
        self.title = str(t)
        self.keep = str(k)
       
    def get_keep(self):
        return self.keep
    def get_str(self):
        if self.title == 'imported':
            return (self.title + " " + self.url )
        return self.title + " " + self.year + " " + self.director

class MainController(ab_Controller):
    def __init__(self, model):
        self.model = model
        self.response = None
        self.waiting = False

    def new_load(self, v, url):
        self.loaddata = LoadData(v, url)

    def set_view(self, v):
        self.view = v

    def request_search(self, query):
        return InitialSearch().get_search(query)
    
    def get_adv_search(self, q1, q2, q3, q4):
        return InitialSearch().get_adv_search(q1, q2, q3, q4)

    def gather_data(self, l):
        for item in l:
            if item.url.startswith("http"):
                self.model.build_df(item, "url")
            else:
                returnstr = self.model.build_df(item.url, "path").tolist()
                if isinstance(returnstr, list):
                    CheckColumns(self.view, self).check_columns(self, self.model.d.df.columns , self.model.d.df.iloc[0])
                    
        self.model.build_report()
        self.view.new_vis_window(self.model.df) 
    
class LoadData(ab_Controller):
    def __init__(self, v, url):
       self.parentview = v
    def create_MovieInfo(self, url):
        return MovieInfo(url, 'imported', 'imported', 'imported', 'keep', 'imported')
        
         
class InitialSearch(ab_Controller):
    def __init__(self):
        self.target ='https://www.imdb.com/title'
        self.hd = { 'Accept-Language' : 'en-US,en;q=0.5' , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        self.session = HTMLSession()
        self.session.headers.update(self.hd)

    

    def getResponse(self, query):
        
        try:
            response = self.session.get(query, headers = self.hd)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

         
    def get_search(self, query):
        original_query = query
        query = ("https://www.google.com/search?q=" + "imdb" 
                              + query + "reviews")
        self.response = self.getResponse(query)
        self.links = list(self.response.html.absolute_links)

        for url in self.links[:]:
            if not (url.startswith(self.target)) or not (url.endswith('fullcredits')):
                self.links.remove(url)
        self.movielist = []
        for url in self.links[:]:
            thismovie = self.get_info_no_filter(url, original_query)

            if (thismovie.get_keep() != 'keep'):
                self.links.remove(url)
            else:
                self.movielist.append(thismovie)
        for movie in self.movielist[:]:
            movie.url= movie.url[:len(url)-11]
            movie.url= movie.url+'reviews'
        return self.movielist

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
        
    def filter_by(self, url, q1, dir, y1, q4):
        
        n_response = requests.get(url, headers=self.hd)
        page = BeautifulSoup(n_response.content, 'html.parser')
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

        if (q4 == ''):
            k_q4 = 'ignore'

        if (d != dir) or (year != y1) or (q4 not in castlist):
            return MovieInfo(url, q1,year,d, 'keep', castlist)
        else:
            return MovieInfo(url, q1, year, 'ignore', castlist)
        
    def get_info_no_filter(self, url, query):
        
        hd =  {'Accept-Language' : 'en-US,en;q=0.5' , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
        n_response = requests.get(url, headers= hd)
        page = BeautifulSoup(n_response.content, 'html.parser')
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
        castlist= []
        cast = page.find_all('td', class_='primary_photo')
        for person in cast:
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
        return MovieInfo(url, query,year,d, 'keep', castlist)

class CheckColumns(ab_Controller):
    def __init__(self, v, c):
        self.view = v
        self.main_cont = c
    
    def check_columns(self, main_cont , titles, row1):
        self.view.new_col_window( titles, row1)
        pass #self.main_cont,
                
