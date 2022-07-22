from abc import ABC, abstractmethod
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import pearsonr

class ab_Model(ABC):
    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def build_df(self): pass

class DFBuilder(ABC):
    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def build_dataset(self, str): pass


class ScrapeData(DFBuilder):
    def __init__(self):
        self.headers = { 'Accept-Language' : 'en-US,en;q=0.5' 
                       , 'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
    def get_response(self, url):
        try:
            
            response = requests.get(url, headers=self.headers)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    
    def build_dataset(self, url):
        
        #unf
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
        reviews= (page.find_all('div', class_='text show-more__control'))
        #print(reviews)
        
        temp_review = str()
        
        for i in reviews:
            r = len(i.contents)
            for j in range(r):
                temp_review += (i.contents[j].text)
            reviews_list.append(temp_review)
            temp_review = ""
        return reviews_list
    #unimplemented
    def find_title():
        pass



class LoadData(DFBuilder):
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.columnlist = ['review_score', 'review_date', 'review_text',
                          'title', 'sentiment', 'sentiment_score', 'score_difference']
    def build_dataset(self, path): 
        
        for column in new_df.columns:
            if column not in columnlist:
                
                return ["AssignCol", self.new_df.columns]
            #begin building df and normalizing review scores
            #remove unscored rows
        df = df[df['review_score'].apply(lambda x: isinstance(x, str))]
        #theres probably a way to do all of these in one...
        lambda_letter_a = lambda x: '1.0' if x.startswith('A') else x
        lambda_letter_b = lambda x: '.8' if x.startswith('B') else x
        lambda_letter_c = lambda x: '.6' if x.startswith('C') else x
        lambda_letter_d = lambda x: '.4' if x.startswith('D') else x
        lambda_letter_f = lambda x: '.2' if x.startswith('F') else x

        #making our temporary df of normalized review scores
        df2 = df.review_score.apply(lambda_letter_a).apply(lambda_letter_b).apply(lambda_letter_c).apply(lambda_letter_d).apply(lambda_letter_f)
        df2 = df2.to_frame()

        #drop review column from original df and add our normalized one
        df = df.drop('review_score', axis=1) 
        df2col=df2['review_score']
        df = df.join(df2col)
        
        #preparing to analyze review_score column
        sia = SentimentIntensityAnalyzer()
        df["sentiment_score"] = None
        df["sentiment"] = None
        df["score_difference"]= None
        
        for (columnName, columnData) in df.iteritems():
            if(columnName not in self.columnlist):
                df = df.drop(columnName, axis=1)
        for index, row in df.iterrows():
            try:
                sentiment = obj.polarity_scores(str(row['review_content']))
                norm_sentiment = ((sentiment['compound'])+1)/2
                row['sentiment_score'] = norm_sentiment
        
                if norm_sentiment > .55:
                    row['sentiment'] = 'pos'
                elif norm_sentiment < .45:
                    row['sentiment'] = 'neg'
                else:
                    row['sentiment'] = 'neutral'
            
                row['score_difference'] = row['review_score']-row['sentiment_score']
            except:
                pass
        #get correlation, average scores, etc   save to .txt
        

        for index, row in selfdf2.iterrows():
            try : row['review_score'] = eval(row['review_score'])
            except: pass

        return df

    
class DataModel(ab_Model):

    def __init__(self):
        self.df= pd.DataFrame({'review_score', 
                          'review_date', 'review_text',
                          'title', 'sentiment', 'sentiment_score', 'score_difference'})
        
    def build_df(self, item , s):
        if s == "url":
            self.d = ScrapeData()
            self.df.append(d.scrape_reviews(item))
        elif s == "path":
            self.d = LoadData()
            returned_df = d.load_dataset(item)
            if returned_df == "AssignCol":
                return #unfinished
            self.df.append(d.load_dataset(item))
        
    def visualize_data(self, vistype):
        pass

    def build_report(df):
        pass
    


        