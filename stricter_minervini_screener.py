# -*- coding: utf-8 -*-
"""Stricter_Minervini_Screener.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zhXK0Nu3S1NbxuXjUB0RowocnJYhG-YV
"""

# Import libraries
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import tkinter as Tk
#from tkinter.filedialog import askopenfilenam

# Install Yahoo Finance's library
!pip install yfinance

import yfinance as yf

# Initialize starting and ending timeframe
yf.pdr_override()
start = dt.datetime(2019,1,1)
now = dt.datetime.now()

# Import Excel file containing every public company's ticker symbol
from google.colab import files
uploaded = files.upload()

# Read the Excel file
stocklist = pd.read_excel('allstocks.xlsx')

Price = stocklist['Price']
RS_rating = stocklist['RS Rating']
Volume = stocklist['Vol. (1000s)']

Price_over_15 = stocklist[Price > 15]
stocklist = Price_over_15

RS_rating_over_70 = stocklist[RS_rating > 70]
stocklist = RS_rating_over_70

Volume_over_400k = stocklist[Volume > 400]
stocklist = Volume_over_400k

Volume_over_400k

# Create a list to add specific data
technical_list = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High", "21 Day EMA"])

for i in stocklist.index:

  stock = str(stocklist['Symbol'][i])
  RS_rating = stocklist['RS Rating'][i]

  try:

    df = pdr.get_data_yahoo(stock, start, now)

    #print("Checking "+stock+"...")

  except Exception:

      print("No data on "+stock)

# Array of each SMA used 

sma = [50, 150, 200]

for x in sma:

  sma = x

  # Calculate the three SMAs
  df["SMA_"+str(sma)] = round(df.iloc[:,4].rolling(window=sma).mean(),2)


# Get most recent data from Yahoo Finance

currentClose = df['Adj Close'][-1]
moving_average_50 = df['SMA_50'][-1]
moving_average_150 = df['SMA_150'][-1]
moving_average_200 = df['SMA_200'][-1]
week_low_52 = min(df['Adj Close'][-260:])
week_high_52 = max(df['Adj Close'][-260:])

try:

  # Get 200SMA moving in an uptrend for a month
  moving_average_200_20past = df['SMA_200'][-20]

except Exception:

  moving_average_200_20past = 0

# Current price over 150sma over 200sma

if(currentClose > moving_average_150 and currentClose > moving_average_200):
  condition_1 = True

else:
  condition_1 = False


# 150sma over 200sma

if(moving_average_150 > moving_average_200):
  condition_2 = True

else:
  condition_2 = False


# 200sma in uptrend for more than 1 month

if(moving_average_200 > moving_average_200_20past):
  condition_3 = True

else:
  condition_3 = False


# 50sma over 150sma and 50sma over 200sma

if(moving_average_50 > moving_average_150 and moving_average_50 > moving_average_200):
  condition_4 = True

else:
  condition_4 = False


# Current price over 50sma

if(currentClose > moving_average_50):
  condition_5 = True

else: 
  condition_5 = False


# Current price is 30% higher than the 52-week low

if(currentClose > (1.3*week_low_52)):
  condition_6 = True

else: 
  condition_6 = False


# Current price is within 25% from its 52-week high

if(currentClose >= (0.75*week_high_52)):
  condition_7 = True

else: 
  condition_7 = False


# IBD RS rating over 70

if(RS_rating > 70):
  condition_8 = True

else: 
  condition_8 = False

if(currentClose > moving_average_21):
  condition_9 = True

else:
  condition_9 = False


# If each condition is met, create a list of the stocks that meet all criteria

if(condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7 and condition_8):
  technical_list = technical_list.append({'Stock': stock, "RS_Rating": RS_rating, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, 
                                  "200 Day MA": moving_average_200, "52 Week Low": week_low_52, "52 week High": week_high_52}, ignore_index=True)


print(technical_list)