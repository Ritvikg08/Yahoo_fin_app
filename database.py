'''
Make funtions to work with the database. 
'''
from yf_data import *
from datetime import date,time,datetime
import pymysql
import sys
import openpyxl

# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='ritvik@123',
                         db='Stock_Data')


# create cursor

 

##Connect to the database for pandas
db_connection_str = 'mysql+pymysql://root:ritvik@123@127.0.0.1/Stock_Data'
db_connection = create_engine(db_connection_str)


def numOfDays(date1, date2):
    return (date1-date2).days

##Use this if Database is empty
def addFirstStock(stock_symbol):
    date1 = date.today()
    date2 = date(1970, 1, 1)
    days=numOfDays(date1, date2)
    print(days, "days")
    stock_df=YahooFinanceHistory(stock_symbol,days_back=days).get_quote()
    rows=len(stock_df)
    col1=[stock_symbol]*rows
    col1=pd.DataFrame(col1)
    stock_df.insert(0,"stock_id",col1,True)
    (pd.DataFrame([stock_symbol],columns=['Symbol'])).to_sql("stock_list",db_connection,if_exists='append',index=False)
    stock_df.to_sql("stock_history",db_connection,if_exists='append',index=False)


##Add full stock-data to sql table
def addFullStockData(stock_list: list):
    for stock_symbol in stock_list:
        stock_symbol=stock_symbol.upper()
        print(stock_symbol)
        if(stock_symbol==""):
            print("Please enter a stock symbol")
            return
        date1 = date.today()
        date2 = date(1970, 1, 1)
        days=numOfDays(date1, date2)
        print(days, "days")
        type(stock_symbol)
        stock_df=YahooFinanceHistory(stock_symbol,days_back=days).get_quote()
        print(stock_df)
        col1=[str(stock_symbol)]*days
        col1=pd.DataFrame(col1)
        stock_df.insert(0,"stock_id",col1,True)
        df1=pd.read_sql_table("stock_list",db_connection)
        print(df1.values.tolist())
        if([stock_symbol] in df1.values.tolist()):
            print("Stock already present in the table")
        else:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            (pd.DataFrame([stock_symbol],columns=['Symbol'])).to_sql("stock_list",db_connection,if_exists='append',index=False)
            stock_df.to_sql("stock_history",db_connection,if_exists='append',index=False)
            try:
                x=getadditionalinfo(stock_symbol)
                y=[stock_symbol]+x
                print(y)
                cursor=connection.cursor()
                sql = "INSERT INTO `stock_info` (`Symbol`, `Current Stock Price`, `Sector`,`Industry`, `P/E`, `EPS`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (y[0],float(y[1]),y[2],y[3],float(y[4]),float(y[5])))
                connection.commit()
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
                return
            print("Next entry.")
            print()
    return    

def updateStockDB(stock_symbol):
    #add past few day's data to db for a particular stock
    df1=pd.read_sql_table("stock_history",db_connection)
    print(len(df1))
    df2=df1.loc[df1['stock_id']==stock_symbol]
    x=max(df2['Date'])
    print(x)
    date1 = date.today()
    date2 = x.date()
    days=numOfDays(date1, date2)
    print(days, "days")
    stock_df=YahooFinanceHistory(stock_symbol,days_back=days).get_quote()
    stock_df=stock_df.loc[stock_df['Date']>datetime.combine(date2, time.min)]
    print(stock_df['Date'])
    if(len(stock_df)>0):
        symbol=[stock_symbol]*len(stock_df)
        stock_df['stock_id']=symbol
        stock_df.to_sql("stock_history",db_connection,if_exists='append',index=False)
    else:
        print("Already updated stock history")
    #df1["Date"].max


def updateAllStocksDB():
    df1=pd.read_sql_table("stock_list",db_connection)
    for i in df1["Symbol"]:
        updateStockDB(i)

#Note: Important Use & with dataframes
def get_StockData(symbol:str,from_date:date,to_date:date):
    symbol=symbol.upper()
    # from_date=date(from_date)
    # to_date=date(to_date)
    df1=pd.read_sql_table("stock_history",db_connection)
    df1=df1.loc[df1['stock_id']==symbol]
    df1=df1.loc[(df1['Date']>=datetime.combine(from_date, time.min)) & (df1['Date']<=datetime.combine(to_date, time.min)) ]
    print(df1)

#updateAllStocksDB()
#updateStockDB('AAPL')
#stock_df.to_excel("output.xlsx")
#addFirstStock("FB")
#addFullStockData('AAPL')
#df1=pd.read_sql_table("stock_history",db_connection)
#get_StockData('FB',date(2013,6,1),date(2019,8,1))


def showStockData(symbol):
    df1=pd.read_sql_table("stock_history",db_connection)
    df1=df1.loc[df1['stock_id']==symbol]
    return df1

def showStockList():
    df1=pd.read_sql_table("stock_list",db_connection)
    print(df1)
    #return df1.to_excel()


def addStockMetadata():

    return

#addFullStockData('rs')

""" 

stock_symbol='AAPL'
stock_df=YahooFinanceHistory(stock_symbol,days_back=365*20).get_quote()
col1=[stock_symbol]*365
col1=pd.DataFrame(col1)
stock_df.insert(0,"stock_id",col1,True)

df1=pd.read_sql_table("stock_list",db_connection)
if(df1['Symbol'].any()!=stock_symbol):
    (pd.DataFrame([stock_symbol],columns=['Symbol'])).to_sql("stock_list",db_connection,if_exists='append',index=False)
    stock_df.to_sql("stock_history",db_connection,if_exists='append',index=False)
    
else:
    print("Stock already present in the table")     """

#df_full=pd.read_sql_table("stock_history",db_connection)
#df_full=df_full[['stock_id','Date','Adj Close']]#pd.DataFrame([df_full['stock_id'],df_full['Date'],df_full['Adj Close']])
#df_full.to_excel('output.xlsx')



