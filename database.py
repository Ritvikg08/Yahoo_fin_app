'''
Make funtions to work with the database. 
'''
from yf_data import *
from datetime import date
 

##Connect to the database
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
def addFullStockData(stock_symbol):
    date1 = date.today()
    date2 = date(1970, 1, 1)
    days=numOfDays(date1, date2)
    print(days, "days")
    stock_df=YahooFinanceHistory(stock_symbol,days_back=days).get_quote()
    print(stock_df)
    col1=[stock_symbol]*days
    col1=pd.DataFrame(col1)
    stock_df.insert(0,"stock_id",col1,True)
    df1=pd.read_sql_table("stock_list",db_connection)
    if(df1['Symbol'].any()!=stock_symbol):
        (pd.DataFrame([stock_symbol],columns=['Symbol'])).to_sql("stock_list",db_connection,if_exists='append',index=False)
        stock_df.to_sql("stock_history",db_connection,if_exists='append',index=False)    
    else:
        print("Stock already present in the table")

def updateStockDB(stock_symbol):
    pass
def updateAllStocksDB():
    pass    

    
#stock_df.to_excel("output.xlsx")
#addFirstStock("FB")
addFullStockData('AAPL')
#df1=pd.read_sql_table("stock_history",db_connection)





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


#print(df1)
#stock_df.to_excel("output.xlsx")
