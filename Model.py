from abc import ABC, abstractmethod
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import pearsonr
from datetime import datetime
import time
import random
import numpy as np
import mechanicalsoup

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
                       , 'User-agent' : 'Mozilla/5.0' }

    def get_response(self, url):
        
        self.browser= mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0')

        return self.browser.open(url)
        
        #try:
            #time.sleep(13 - random.randint(0,6))
            #response = requests.get(url, headers=self.headers)
            #return response
        #except requests.exceptions.RequestException as e:
            #print(e)

    
    def build_dataset(self, url):
        response = self.get_response(url.url)
        #button = self.browser.page.find_elements_by_class_name('load-more-trigger')
        #button.click()
        anlyz = SentimentIntensityAnalyzer()

        soup = BeautifulSoup(response.content , 'html.parser')
        ratings_list = []
        reviews_list = []
        dates_list = []
        helpful_list1 = []
        helpful_list2 = []
        sentiment_list = []
        sentiment_rating = []
        norm_sentiment = []
        score_difference = []
        
        #get list of ratings
        ratings = soup.find_all('div', class_='lister-item-content')

        for i in ratings:
            ratings_list.append(str(i)[442:444].replace("<", ""))
        
        #get list of review text
        reviews = soup.find_all('div', class_='text show-more__control')

        temp_review = str()
        for i in reviews:
            if 'rating-other-user-rating' not in i:
                r = len(i.contents)
                for j in range(r):
                    temp_review += (i.contents[j].text)
                reviews_list.append(temp_review)
                temp_review = ""

        #get list of dates
        review_dates = soup.find_all('span', class_='review-date')

        for i in review_dates:
            dates_list.append(i.contents[0])
        for r in range(len(dates_list)):
            dates_list[r] = str(datetime.strptime(dates_list[r], '%d %B %Y').date())

        # get list of helpfulness rating
        h_rating = soup.find_all('div', class_='actions text-muted')

        for i in h_rating:
            helpful_list1.append(i.contents)
            i= str(i.contents)
            i= ''.join(i.split())
            i= i.replace(',','')
            i= i[4:18]
            n1 = ''
            n2 = ''
            switch = False
            hitsecondn = False

            for c in i:
                if c.isnumeric():
                    if switch == False:
                        n1 = n1 + c
                    else:
                        hitsecondn = True
                        n2 = n2+c
                else:
                    switch = True
                    if hitsecondn == True:
                        n3 = n1+ '/' + n2
                        n3 = eval(n3)
                        helpful_list2.append(n3)

                        break
        #analyze text
        for r in range(len(reviews_list)):
            sentiment_list.append(anlyz.polarity_scores(reviews_list[r])['compound'])

            if (sentiment_list[r] > 0):
                sentiment_rating.append("pos")
            elif (sentiment_list[r] <= 0):
                sentiment_rating.append("neg")
            else:
                sentiment_rating.append("neutral")
    
    #remove unscored reviews
        remove = []
        for i in range(len(ratings_list)):
            if (ratings_list[i][0].isnumeric()):
                pass
            else:
                remove.append(i)
        for r in sorted(remove, reverse = True):

            del ratings_list[r]
            del reviews_list[r]
            del dates_list[r]
            del helpful_list2[r]
            del sentiment_list[r]
            del sentiment_rating[r]
        
        for i in range(len(ratings_list)):
            ratings_list[i] = eval(ratings_list[i] + '/10')

        for item in sentiment_list:
            nitem = (item+1)/2
            norm_sentiment.append(nitem)

        for r in range(len(ratings_list)):
            score_difference.append(abs(norm_sentiment[r] - ratings_list[r]))
        
        review_length = []
       
        #for i in reviews_list:
            #review_length.append(len(str(i)))

        #assemble DataFrame from lists
        df = pd.DataFrame(dates_list, columns = ['review_date'])
        df['review_content'] = reviews_list
        df['review_score'] = ratings_list
        df['sentiment_score'] = norm_sentiment
        df['sentiment'] = sentiment_rating
        df['score_difference'] = score_difference
        df['review_length'] = score_difference

        for index, row in df.iterrows():
            row['review_length'] = len(str(row['review_content']))
        
        return df

class LoadData(DFBuilder):
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.columnlist = ['review_date', 'review_content', 'review_score', 
                           'sentiment', 'sentiment_score', 'score_difference', 'review_length']
    def build_dataset(self, path): 
        
        
        self.df = self.df[self.df['review_score'].apply(lambda x: isinstance(x, str))]
        #theres probably a way to do all of these in one...
        lambda_letter_a = lambda x: '1.0' if x.startswith('A') else x
        lambda_letter_b = lambda x: '.8' if x.startswith('B') else x
        lambda_letter_c = lambda x: '.6' if x.startswith('C') else x
        lambda_letter_d = lambda x: '.4' if x.startswith('D') else x
        lambda_letter_f = lambda x: '.2' if x.startswith('F') else x

        #making our temporary df of normalized review scores
        df2 = self.df.review_score.apply(lambda_letter_a).apply(lambda_letter_b).apply(lambda_letter_c).apply(lambda_letter_d).apply(lambda_letter_f)
        df2 = df2.to_frame()

        #drop review column from original df and add our normalized one
        self.df = self.df.drop('review_score', axis=1) 
        df2col=df2['review_score']
        self.df = self.df.join(df2col)
        
        #preparing to analyze review_score column
        obj = SentimentIntensityAnalyzer()
        self.df["sentiment_score"] = None
        self.df["sentiment"] = None
        self.df["score_difference"]= None
        self.df["review_length"]= None
        self.df['review_score']
        for (columnName, columnData) in self.df.iteritems():
            if(columnName not in self.columnlist):
                self.df = self.df.drop(columnName, axis=1)


        for index, row in self.df.iterrows():
            row['review_score']= eval(row['review_score'])
            sentiment = obj.polarity_scores(str(row['review_content']))
            norm_sentiment = ((sentiment['compound'])+1)/2
            row['sentiment_score'] = norm_sentiment
        
            if norm_sentiment > .5:
                row['sentiment'] = 'pos'
            elif norm_sentiment <= .5:
                row['sentiment'] = 'neg'
            else:
                row['sentiment'] = 'neutral'
            #print(row['review_score'])
            
            row['score_difference'] = row['review_score']-row['sentiment_score']
            row['review_length'] = len(str(row['review_content']))
            

        #get correlation, average scores, etc   save to .txt
        

        for index, row in self.df.iterrows():
            try : row['review_score'] = eval(row['review_score'])
            except: pass
        
        return self.df

    
class DataModel(ab_Model):

    def __init__(self):
        self.df= None
    
    def reset_df(self):
        self.df = None
    def build_df(self, item , s):
        print(self.df)
        if s == "url":
            self.d = ScrapeData()
            df2 =self.d.build_dataset(item)
            #self.df.append(df2)
            self.df = pd.concat([self.df, df2], join = 'outer')
            print(df2)
            print(self.df)
            pass
        elif s == "path":
            item = ''.join(item.split())
            item = item[:-16]
            item = item[2:]
            print(item)
            self.d = LoadData(item)
            df2 = self.d.build_dataset(item)
            #if returned_df[0] == "AssignCol":
                
                #return self.d.df.columns
            #column names not in column list (remove columns that already have a match)
            self.df = pd.concat([self.df, df2], join = 'outer')
            #print(self.df)
        
    def visualize_data(self, vistype):
        pass
    def save_dataframe(self, df):
        print(df)
        filename = ("Dataset-"+ str(datetime.now())+ ".csv")
        filename = ''.join(filename.split())
        filename = filename.replace(":", "")

        df.to_csv(filename)


    def build_report(self):
        reportname = ("report-"+ str(datetime.now())+ ".txt")
        reportname = ''.join(reportname.split())
        reportname = reportname.replace(":", "")
        numperiods = reportname.count('.')
        reportname= reportname.replace('.', "", numperiods - 1)
        print(reportname)

        scorecorrelation = str(pearsonr(self.df['review_score'], self.df['sentiment_score']))
        summary = "number of rows = " + str(self.df.shape[0]) + "\nAverate user rating = " + str(self.df['review_score'].mean()) +'\nuser rating std deviation ='+ str(np.std(self.df['review_score']))+"\n\nAverage Sentiment score = " + str(self.df['sentiment_score'].mean()) +"\nSentiment score std deviation = " + str(np.std(self.df['sentiment_score'])) +"\n\nAverage score difference = " + str(self.df['score_difference'].mean())+"\nstd deviation in score difference = " + str(np.std(self.df['score_difference']))
        summary = summary + "\n" + scorecorrelation
        
        
        
        with open(reportname, 'w')as f:


            f.write(summary)
    


       