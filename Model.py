import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class DataModel:
    
    def __init__(self):
        self.df_list = list()
        self.df_temp = None

    def get_response(self, url):
        try:
            headers = { 'Accept-Language' : 'en-US,en;q=0.5' 
                       , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    def scrape_reviews(self, url):
        self.response = get_response(url)
        
        page = BeautifulSoup(self.response.content, 'html.parser')
        reviews = page.find_all('div', class_='review-container')
        
        #need to remove tags from results still

        moviename = page.find('div', class_="parent").get_text()
        #reviewtext=             in class= 'text show-more_control'
        reviewtexts = page.find_all('div', class_='text show-more_control').get_text()
        #score=                  in class= 'rating-other-user-rating'
        scores= page.find_all('div', class_='rating-other-user-rating').get_text()
        #date=                   in class='review date
        dates= page.find_all('div', class_='review-date').get_text()
        dates = dates
        #helpfulpercentage=      in class='actions text-muted'

        self.df_temp= pd.DataFrame({'score': scores, 
                          'dates' : dates, 'reviewtexts' : reviewtexts})
        self.df_temp['movie'] = moviename

        self.df_list.append(df_temp)

        return (str(moviename + str(len(reviews))))

    def load_dataset(self, path):
        self.df_temp = pd.read_csv(path)
        
        # need to check to make sure columns match 
        return (str(moviename + str(len(reviews))))

        #return "column check"

    def append_temp(self):
        self.df_list.append(df_temp)