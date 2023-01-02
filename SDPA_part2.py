#!/usr/bin/env python
# coding: utf-8

# #           Project: Stock data analysis of Google

# In[1]:


#import library
import requests #library to deal requests
import numpy as np #library to analyse data
import pandas as pd #library to deal with vectorized data
import random #generate random numbers
import time
import math #calculation
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import kstest
from scipy import stats
from pandas import DataFrame,Series
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf #ACF and PACF test
import statsmodels.api as sm  #conduct the ARIMA model
from sklearn import linear_model  #conduct the liner model


# ## 1.Data preparation

# In[2]:


#Get all the stock data of Google from 2004 to 2022
import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

querystring = {"period1":"978048000","period2":"1672272000","symbol":"GOOG","frequency":"1d","filter":"history"}

headers = {
	"X-RapidAPI-Key": "3508c05f91mshd060442ffb95cc5p17fd97jsncd23e96b082c",
	"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

#Get all the data of Microsoft from 2004 to 2022
import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

querystring = {"period1":"978048000","period2":"1672272000","symbol":"MSFT","frequency":"1d","filter":"history"}

headers = {
	"X-RapidAPI-Key": "3508c05f91mshd060442ffb95cc5p17fd97jsncd23e96b082c",
	"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

response1 = requests.request("GET", url, headers=headers, params=querystring)



# ## 2.Data Cleaning

# In[3]:


#Transform Google's json file to a data frame
data1= response.json()["prices"]
Goog = pd.json_normalize(data1)
#reverse the original data, make the data begin from 2004
Goog = Goog.reindex(index=Goog.index[::-1])
Goog = Goog.reset_index(drop = 'True')
Goog.head()


# In[4]:


#Transform Dow Jones's json file to a data frame
data2= response1.json()["prices"]
MSFT = pd.json_normalize(data2)
#reverse the original data
MSFT = MSFT.reindex(index=Goog.index[::-1])
MSFT = MSFT.reset_index(drop = 'True')
MSFT.head()


# In[5]:


#Change the timestamp to a normal date of Google
Goog['date'] = pd.to_numeric(Goog['date'])
Goog['date'] = Goog['date'].apply(lambda x: time.strftime('%Y-%m-%d', time.localtime(x)))
Goog['date'] = pd.to_datetime(Goog['date'], format="%Y-%m-%d")
Goog.head()


# In[6]:


#Change the timestamp to a normal date of MSFT
MSFT['date'] = pd.to_numeric(MSFT['date'])
MSFT['date'] = MSFT['date'].apply(lambda x: time.strftime('%Y-%m-%d', time.localtime(x)))
MSFT['date'] = pd.to_datetime(MSFT['date'], format="%Y-%m-%d")
MSFT.head()


# In[7]:


#delete the useless column of Goog
Goog= Goog.dropna(axis=1,thresh=2000) #There are more than 4000 rows of data in total, delete all the columns with more than 2000 null values

#dealing with missing data of Goog 
Goog.isnull().any(axis=1) #True means null value

#delete all the rows with True of Goog
Goog.loc[Goog.isnull().any(axis=1)]
drop_index = Goog.loc[Goog.isnull().any(axis=1)].index
Goog.drop(labels=drop_index,axis=0)

#delete the repeat date
Goog = Goog.drop_duplicates(subset = 'date')
Goog


# In[8]:


#delete the useless column of MSFT
MSFT= MSFT.dropna(axis=1,thresh=2000) #There are more than 4000 rows of data in total, delete all the columns with more than 2000 null values

#dealing with missing data of MSFT
MSFT.isnull().any(axis=1) #True means null value

#delete all the rows with True of MSFT
MSFT.loc[MSFT.isnull().any(axis=1)]
drop_index = MSFT.loc[MSFT.isnull().any(axis=1)].index
MSFT.drop(labels=drop_index,axis=0)

#delete the repeat date
MSFT = MSFT.drop_duplicates(subset = 'date')
MSFT


# In[9]:


#Modify the column name
Goog.columns=['date','open_GOOG','high_GOOG','low_GOOG','close_GOOG','volume_GOOG','adjclose_GOOG']
MSFT.columns=['date','open_MSFT','high_MSFT','low_MSFT','close_MSFT','volume_MSFT','adjclose_MSFT']

#merge the data
Stock = pd.merge(Goog,MSFT,on='date',how = 'right')

#Add two columns to calculate the Trading value of the two companies
Stock.insert(7,'TradingValue_GOOG_billion',((Stock['high_GOOG']+Stock['low_GOOG'])/2*Stock['volume_GOOG'])/100000000)
Stock.insert(14,'TradingValue_MSFT_billion',((Stock['high_MSFT']+Stock['low_MSFT'])/2*Stock['volume_MSFT'])/100000000)

#delete the repeat date
Stock = Stock.drop_duplicates(subset = 'date')

#delete all the missing data
Stock = Stock.dropna(axis=0)
Stock


# In[10]:


#Saving files as  csv
Stock.to_csv('./Stock.csv')


# ## Exploratory analysis

# In[11]:


Stock.describe()


# #### According to the table above, Microsoft's historical average stock price is approximately twice that of Google, and Microsoft's all-time high stock price of 344.62 is more than twice as high as Google's 151.86. In addition, the historical daily trading volume of Microsoft stock is 272 billion, while Google is only 171.6 billion, but this does not mean that Microsoft's trading is more active than Google's, due to Google's higher trading volume than Microsoft. The above data does not indicate that company's stock is performing better, we need to calculate the rise and fall of the stock price to get the result.

# In[12]:


#calculate the RF_rate 
Goog_close = Stock['close_GOOG']
MSFT_close = Stock['close_MSFT']
#insert the RF_rate
Goog_RF_rate = (Stock['open_GOOG']-Stock['close_GOOG'])/Stock['open_GOOG']*100
Stock.insert(8,'Goog_RF_rate',Goog_RF_rate)
MSFT_RF_rate = (Stock['open_MSFT']-Stock['close_MSFT'])/Stock['open_MSFT']*100
Stock.insert(15,'MSFT_RF_rate',MSFT_RF_rate)


# In[13]:


#Use the histogram to see the RF_rate distribution of GOOG
plt.hist(x = Stock.Goog_RF_rate, bins=20 , color='steelblue',edgecolor='black')

#Add x-axis and y-axis labels
plt.xlabel('RF_rate(%)')
plt.ylabel('Number of frequencies')

#Add a title
plt.title('Figure1: GOOG RF_rate distribution ')

plt.show()


# In[14]:


#Use the histogram to see the RF_rate distribution of GOOG
plt.hist(x = Stock.MSFT_RF_rate, bins=20 , color='steelblue',edgecolor='black')

#Add x-axis and y-axis labels
plt.xlabel('RF_rate(%)')
plt.ylabel('Number of frequencies')

#Add a title
plt.title('Figure2: MSFT RF_rate distribution ')

plt.show()


# #### According to Figures 1 and 2, Google's stock price single-day RF_rate distribution is right-skewed, while Microsoft's stock price single-day RF_rate distribution is left-skewed. This means that Microsoft stock price has more single-day up days than Google. However, Microsoft's outliers are more extreme than Google's, and Microsoft's maximum one-day declines are more extreme than Google's.

# In[15]:


#Plot a line graph of the stock prices of the two companies
year = pd.to_datetime(Stock.date,format = "%Y")
plt.plot(year,Stock['open_GOOG'],label = 'GOOG')
plt.xlabel('Year')
plt.ylabel('Price(USD)')
plt.plot(year,Stock['open_MSFT'],label = 'MSFT')
plt.title('Figure 3: Stock price of GOOG&MSFT')
plt.legend()


# #### According to figure3, the stock prices of both companies have been rising since 2004 until the peak at the end of 2021, after which both companies' stock prices have been falling to the present.

# In[16]:


#Plot a scatter plot to see if Trading Volume and RF_rate are correlated
plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(Stock.TradingValue_GOOG_billion,Stock.Goog_RF_rate,color = 'r',label = 'GOOG',s =5)
plt.scatter(Stock.TradingValue_MSFT_billion,Stock.MSFT_RF_rate,color = 'b',label = 'MSFT',s=5)
plt.xlabel('Trading value(billion)')
plt.ylabel('RF_rate(%)')
plt.title('Figure 4: Scatter plot of trading value and RF_rate')


# #### According to figure 4, there is no significant correlation between RF_rate and Trading value, i.e. Trading value does not affect whether the stock is up or down on that day.

# In[17]:


#Analyze if there is a correlation between GOOG's stock price and MSFT's
plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(Stock.Goog_RF_rate,Stock.MSFT_RF_rate,color = 'b')
plt.xlabel('GOOG_RF_rate(%)')
plt.ylabel('MSFT_RF_rate(%)')
plt.title('Figure 5: Scatterplot of Google RF_rate and Microsoft RF_rate')


# #### According to figure 5, there is a strong linear correlation between Google's RF_rate and Microsoft's RF_rate, i.e., Google's stock price and Microsoft's price affect each other. We can further calculate the correlation coefficient between the two.

# In[18]:


#Calculate their correlation coefficients
r,p = stats.pearsonr(Goog_RF_rate,MSFT_RF_rate)
print('Correlation coefficient is = %6.3f,p-value = %6.3f'%(r,p))


# #### There is a significant correlation between Google's RF_rate and Microsoft's RF_rate, and the correlation coefficient is 0.58, which is a moderate correlation.

# ## 3.Question the data

# ### 3.1 Suppose there are two stock strategies, one is to buy the 100 stock on the last trading day of each month and then sell it on the last trading day of each year, and the other is to calculate the 5-day SMA and 30-day SMA of the stock and buy the stock when the 5-day SMA shows an upward trend and crosses the 30-day SMA, and sell the stock when the 5-day SMA shows a downward trend and crosses the 30-day SMA. The returns of the two trading strategies are calculated separately and compared. （Use the expenses of the first strategy as the principal of the second strategy, and for GOOG stock only）

# #### 3.1(1) Monthly Trading Strategy

# In[19]:


#Get month data
Stock = Stock.set_index('date').sort_index() #Set date to index
new_Stock = Stock['2004-12':'2022-12']

#Extract the specified data from the original data according to the month
Stock_monthly = new_Stock.resample('M').first()
Stock_monthly.head()


# In[20]:


#Calculate the cost of buying a stock
cost_GOOG = Stock_monthly['open_GOOG'].sum()*100
#Calculate the money after selling the stock
Stock_year  =new_Stock.resample('A').last()

money_GOOG = Stock_year['open_GOOG'].sum()*2160

#Calculate the income
income_GOOG = money_GOOG - cost_GOOG
print('The income of GOOG is',income_GOOG.round())


# #### 3.1(2) Double Averaging Strategy

# In[21]:


#MA5
ma5_GOOG = Stock['close_GOOG'].rolling(5).mean()

#MA30
ma30_GOOG = Stock['close_GOOG'].rolling(30).mean()


# In[22]:


#Get the death_date, i.e. when MA5 is trending down and crosses MA30(death cross),When the MA5 is trending upwards over the MA30(golden cross)
ma5_GOOG = ma5_GOOG[30:]
ma30_GOOG = ma30_GOOG[30:]

#golden cross left ma5<ma30,right ma>30,dead cross left ma5>ma30,right ma<30
s1 = ma5_GOOG<ma30_GOOG
s2 = ma5_GOOG>ma30_GOOG

Stock1 = Stock[30:]
#Conditions for determining a dead cross
death_ex = s1&s2.shift(1) #Returns True only if True and True of s2.shift(1) meet

#Get the death date
death_date = Stock1.loc[death_ex].index
death_date


# In[23]:


#Determine the golden cross condition and obtain the date of the cross
golden_ex = ~(s1|s2.shift(1)) #Determine the golden fork condition, ~ represents the inverse, | represents the or condition, as long as the True value appears, then return True
golden_date = Stock1.loc[golden_ex].index
golden_date


# In[24]:


#Merge the dates of golden crosses and dead crosses and mark them
s1 = Series(data=1,index = golden_date)
s2 = Series(data=0,index = death_date) #1 is a golden cross marker, 0 is a dead cross marker

s = s1.append(s2)
s = s.sort_index()
s #the dates of golden and dead crosses


# In[25]:


#Using the  Double Averaging Strategy
start_money = cost_GOOG #Principal amount, immutable
money = start_money  #Variable, buy and sell stock operations
hold = 0 #Number of shares held, 100 shares for 1 lot

for i in range(0,len(s)): #i denotes the implicit index in s the Series, time is the display index
    if s[i] ==1: #golden cross
        #Buy as many stocks as possible based on the principal
        time = s.index[i] #the date of golden cross
        p = Stock1.loc[time]['open_GOOG'] #open price
        lot_count = money//(p*100)  #Calculate how many shares were bought
        hold = lot_count*100
        money -= (hold*p) #Subtract the money spent on buying stocks from money
        
    else:
        #Sell the bought shares
        death_time = s.index[i]
        p_death = Stock1.loc[death_time]['open_GOOG']
        money += (p_death*hold)#Add the proceeds from the sale of shares to money
        hold = 0 #Clear the hold to 0 to start the next loop
        
#Add the remaining stocks to the earnings and determine whether the last day is a golden cross or a dead cross
last_money = money + hold*Stock1['close_GOOG'][-1]
print('The income of GOOG by using this strategy is',(last_money-start_money).round())
                                 


# #### Based on the results of the two strategies above, it comes out to be 821,204 USD for the same amount of money spent. The first strategy focuses on regular money management, which is less risky, but also has a smaller income of  774,382 USD. The second trading strategy earned  16,692,428 USD, which is much higher than the first strategy's income.

# ### 3.3 Try to predict the stock price in the next 30 days using time series models (ONLY for GOOG)

# #### ARIMA Model------ARIMA model is a classic analytical model of time series, divided into AR (Auto Regression) part, which is used to describe the relationship between the current value and the historical value, using the variable's own historical time data to predict itself, and MA (Moving Average) part, in the AR model, if the series is not a white noise, it is usually considered to be a moving average of order q

# In[26]:


#Splitting data sets
Stock_1 = Stock['close_GOOG'].resample('W-TUE').mean()#Weekly frequency as a standard
Stock_train = Stock_1['2008':'2022']
# Differentiate the data to make the data smooth and meet the requirement of smoothness
stock_dif = Stock_train.diff(1).dropna()
plt.figure()
plt.plot(stock_dif)
font_Loc=''
plt.title('Figure 6: First order differential') 


# #### The time series is essentially smooth after performing differencing. We can perform ACF and PACF tests to further determine whether the first-order difference satisfies the smoothness requirement.

# In[27]:


#Plot ACF 
ACF = plot_acf(stock_dif, lags=20)
plt.title('Figure 7: ACF plot')
plt.show()

#Plot PACF
PACF = plot_pacf(stock_dif,lags = 20)
plt.title('Figure 8:PACF')
plt.show()


# #### According to Figures 7 and 8, the results already fall within the confidence interval when performing the first-order difference (blue area in the figure), so it can be determined that performing the first-order difference is reliable and valid.Next, the ARIMA model can be performed

# In[29]:


#conduct the model
model = sm.tsa.arima.ARIMA(Stock_train, order=(1,1,1))# Training model, order representation (p,d,q)
result = model.fit()

#make the predication
pred = result.predict('2022-12-28','2023-01-27',dynamic=False,type='levels')


# In[30]:


#Plot's predicted results using the ARIMA model
plt.figure(figsize=(8,8))
plt.xticks(rotation = 45)
plt.plot(pred)
plt.plot(Stock_train['2022-10-20':'2022']) #Sliced data makes the presentation of prediction results more obvious
plt.title('Figure 9:GOOG stock price results for the next 30 days using ARIMA')
plt.show()


# In[49]:


prediction


# ### 3.3In response to the conclusion that there is a positive correlation between the stock prices of the two stocks above, we continue to extend the analysis and need to obtain more data on the stocks for correlation analysis

# In[43]:


from yahoo_fin.stock_info import get_data


# In[71]:


#Transform Google's json file to a data frame
data2= response.json()["prices"]
data3 = pd.json_normalize(data2)
#reverse the original data, make the data begin from 2004
data3


# In[ ]:




