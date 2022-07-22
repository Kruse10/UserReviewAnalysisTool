import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import nltk
from vaderSentiment.vaderSentiment import *


class ScrapeData:

    def get_response(self, url):
        try:
            headers = { 'Accept-Language' : 'en-US,en;q=0.5' 
                       , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    
    def scrape_reviews(self, url):
        self.response = self.get_response(url)
        
        self.page = BeautifulSoup(self.response.content, 'html.parser')
        reviews = page.find_all('div', class_='review-container')
        reviews_list = []
        dates_list = []

        self.df_temp= pd.DataFrame({'score': scores, 
                          'dates' : dates, 'reviewtexts' : reviewtexts})
        self.df_temp['movie'] = moviename

        self.df_list.append(df_temp)

        return (str(moviename + str(len(reviews))))
    
    def find_date():
        
        reviewdates= (self.page.find_all('span', class_='review-date'))
        
        for i in reviewdates:
            dates_list.append(i.contents[0])

        for r in range(len(dates_list)):
            print( dates_list[r])
            print("\n")
    
    def find_review_text():
        reviews= (soup.find_all('div', class_='text show-more__control'))
        #print(reviews)
        
        temp_review = str()
        
        for i in reviews:
            r = len(i.contents)
            for j in range(r):
                temp_review += (i.contents[j].text)
            reviews_list.append(temp_review)
            temp_review = ""
        return reviews_list


class DataModel:

    def __init__(self):
        self.df= pd.DataFrame({'review_score', 
                          'review_date', 'review_text',
                          'title', 'sentiment', 'sentiment_score', 'score_difference'})
        
        self.scraper = ScrapeData()
    

    def load_dataset(self, path): 
        self.new_df = pd.read_csv(path)
        for column in new_df.columns:
            if column not in columnlist:
                pass #need to call method to open window to assign labels to existing columns not implemented yet
                return "AssignCol"
        #remove unscored


        df = df[df['review_score'].apply(lambda x: isinstance(x, str))]


        