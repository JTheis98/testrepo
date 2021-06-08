# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 13:24:55 2020

@author: Jake Theis
Homework 4

1. I ran into some issues with displaying the stack bar chart.
I was able to mutate the dataframe using the groupby function 
with no problem but was having errors showing it. I eventually 
resolved it with plt.show() function

2. N/A

"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

BOOKS_DATA_FILE = 'C:/Users/19723/OneDrive - UWSP/2020Fall/DAC111/Datasets/books.csv'

TITLE_COLUMN = 'Title'
AUTHOR_COLUMN = 'Author'
GENRE_COLUMN = 'Genre'
HEIGHT_COLUMN = 'Height'
PUBLISHER_COLUMN = 'Publisher'
COUNT_COLUMN = 'count'

BOOKS_BY_TITLE_OPTION = 1
BOOKS_BY_AUTHOR_OPTION = 2
BOOKS_BY_MIN_HEIGHT_OPTION = 3
BOOKS_BY_PUBLISHER_AND_GENRE_OPTION = 4
BOOKS_BY_GENRE_OPTION = 5
BOOK_HEIGHT_STATS = 6

def main():
    booksData = read_data(BOOKS_DATA_FILE)
    pd.set_option('display.max_colwidth', -1)
    
    while True:
        userInput = get_menu_option()
        
        if userInput == BOOKS_BY_TITLE_OPTION:
            bookTitle = input('Enter a title to search for: ')
            titleData = search_column_text_data(booksData, TITLE_COLUMN, bookTitle)
            bookInfo = join_data(titleData, booksData[AUTHOR_COLUMN])
            print(bookInfo.to_string())
        elif userInput == BOOKS_BY_AUTHOR_OPTION:
            bookAuthor = input('Enter an author to search for: ')
            authorData = search_column_text_data(booksData, AUTHOR_COLUMN, bookAuthor)
            bookInfo = join_data(authorData, booksData[TITLE_COLUMN])
            print(bookInfo.to_string())
        elif userInput == BOOKS_BY_MIN_HEIGHT_OPTION:
            bookHeight = int(input('Enter book minimum height to search for: '))
            heightData = search_column_min_numerical_data(booksData, HEIGHT_COLUMN, bookHeight)
            bookInfo = join_data(heightData, booksData[TITLE_COLUMN])
            bookInfo = join_data(bookInfo, booksData[AUTHOR_COLUMN])
            bookInfo = bookInfo.drop([HEIGHT_COLUMN], axis = 1)
            print(bookInfo.to_string())
        elif userInput == BOOKS_BY_PUBLISHER_AND_GENRE_OPTION:
            plot_stack_bar_chart(booksData, PUBLISHER_COLUMN, GENRE_COLUMN, 'Books by Publisher and Genre')
        elif userInput == BOOKS_BY_GENRE_OPTION:
            booksByGenre = get_column_group_count(booksData, GENRE_COLUMN)
            plot_bar_chart('Genre', 'Counts', booksByGenre[GENRE_COLUMN], 
                       booksByGenre[COUNT_COLUMN], 'Book Counts by Genre')
        elif userInput == BOOK_HEIGHT_STATS:
            bookHeightStats = get_column_statistics(booksData, HEIGHT_COLUMN)
            print(bookHeightStats)
        else:
            break

def get_column_statistics(data, columnName):
    statString = "Statistics"
    
    average = data[columnName].mean()
    statString += "\nAverage: " + str(average) 
    minimum = data[columnName].min()
    statString += "\nMinimum: " + str(minimum)
    maximum = data[columnName].max()
    statString += "\nMaximum: " + str(maximum)
    quartileOne = np.percentile(data[columnName], 25)
    statString += "\nQuartile One: " + str(quartileOne)
    median = np.percentile(data[columnName], 50)
    statString += "\nMedian: " + str(median)
    quartileThree = np.percentile(data[columnName], 75)
    statString += "\nQuartile Three: " + str(quartileThree)
    
    return statString
      
def plot_stack_bar_chart(data, dataForXAxis, dataToBeStacked, title):
    chartData = data.groupby([dataForXAxis, dataToBeStacked])[dataToBeStacked].count().unstack(dataToBeStacked).fillna(0)
    chartData.plot(kind = 'bar', stacked = 'True', title = title)    
    plt.show()
def plot_bar_chart(xlabel, ylabel, xData, yData, title, color = 'green'):
    xPositions = [xPoint for xPoint, _ in enumerate(xData)]
    plt.bar(xPositions, yData, color = color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(xPositions, xData, rotation = 'vertical')
    plt.tight_layout()
    plt.show()
           
def get_column_group_count(data, columnName):
    data = data.groupby([columnName])[columnName] \
    .count().reset_index(name = 'count') \
    .sort_values(['count'], ascending = False) 
    
    return data       

def search_column_text_data(data, columnName, searchText):
    data = data[data[columnName].str.contains(searchText) == True]
        
    return pd.DataFrame(data[columnName])
    
def search_column_min_numerical_data(data, columnName, searchNumber):
    data = data[data[columnName] >= searchNumber]
    
    return pd.DataFrame(data[columnName])

def join_data(firstColumn, secondColumn):
    info = pd.DataFrame(firstColumn).join(secondColumn)
    
    return info 
def get_menu_option():
    userInput = -1
    
    while userInput == -1:
        try:
            print(
'''
Books Data Menu
1. Search Books by Title
2. Search Books by Author
3. Search Books by Minimum Height
4. Graph Total Books by Publisher and Genre
5. Graph Total Books by Genre
6. Display Total Book Height Statistics

'''
                )
            
            userInput = input('Enter an option: (enter q to quit) ')
            
            if userInput == 'q':
                return 0
            
            userInput = int(userInput)
            
            if(not userInput in range(BOOKS_BY_TITLE_OPTION, BOOK_HEIGHT_STATS + 1)):
                print('Invalid Menu Option. Please Try Again')
                userInput = -1
            
        except:
            print('Invalid Menu Option. Please Try Again.')
            userInput = -1
            
    return userInput

def read_data(filename):
    return pd.read_csv(filename)
    

main()
