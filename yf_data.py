import re
from io import StringIO
from datetime import datetime, timedelta,date
import requests
import pandas as pd
import mysql.connector as sql
from sqlalchemy import create_engine
import pymysql
import requests
from bs4 import BeautifulSoup

# stock_symbol =input()
# URL = 'https://in.finance.yahoo.com/quote/'+stock_symbol+'/profile?p='+stock_symbol
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')
# #print(soup)
# x=soup.find(class_="asset-profile-container")

# y=x.get_text().split('Industry:')
# sector=y[0].split('Sector(s):')[1]
# industry=y[1].split('Full-time employees:')[0]
# print(Sector)
# print(Industry)
def getadditionalinfo(stock_symbol: str):
    stock_symbol=stock_symbol.upper()
    URL = 'https://in.finance.yahoo.com/quote/'+stock_symbol+'/profile?p='+stock_symbol
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    x=soup.find(class_="asset-profile-container")
    y=x.get_text().split('Industry:')
    sector=y[0].split('Sector(s):')[1]
    industry=y[1].split('Full-time employees:')[0]
    URL='https://in.finance.yahoo.com/quote/'+stock_symbol+'?p='+stock_symbol
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    x=soup.find(id="quote-header-info")
    #print(x.get_text())
    x=x.get_text()
    x=x.split('Add to watchlist')[1]
    print(x)
    price=float((x.split('.')[0]).replace(',','',1)+'.'+(x.split('.')[1][:2]).replace(',',''))
    print(price)
    x=soup.find(id='quote-summary')
    y=x.get_text()
    a=y.split('PE ratio (TTM)')[1]
    pe=float(a.split('EPS (TTM)')[0])
    eps=float(a.split('EPS (TTM)')[1].split('Earnings date')[0])
    #print(price,sector,industry,pe,eps)
    return [price,sector,industry,pe,eps] 

#print(getadditionalinfo('rs'))

########################################################################
class YahooFinanceHistory:
    timeout = 10
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1d&events=history&crumb={crumb}'

    def __init__(self, symbol, days_back=7):
        self.symbol = symbol
        self.session = requests.Session()
        self.dt = timedelta(days=days_back)

    def get_crumb(self):
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)

    def get_quote(self):
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        now = datetime.utcnow()
        dateto = int(now.timestamp())
        datefrom = int((now - self.dt).timestamp())
        url = self.quote_link.format(quote=self.symbol, dfrom=datefrom, dto=dateto, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), parse_dates=['Date'])

################################
# Using the above class to get a dataframe
#stock_df=YahooFinanceHistory("Inf",days_back=365).get_quote()
#print(date.today())
