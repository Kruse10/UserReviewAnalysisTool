import matplotlib.pyplot as plt
import sys
import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class RatingOverTime(FigureCanvas):
    def __init__(self,parent, df):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        self.ax.plot(df['review_date'], df['review_score'])

        pass

class UserRating_Sentiment(FigureCanvas):
    def __init__(self,parent, df):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        self.ax.plot(df['review_date'], df['review_score'])

        pass

