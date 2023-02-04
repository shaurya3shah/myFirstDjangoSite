import pandas as pd
import yfinance as yf
import sqlalchemy as db
import datetime


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def export_snp(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name} I am going to export all the S&P data collected so far')  # Press ⌘F8 to toggle the breakpoint.

    engine = db.create_engine("mysql://sns:connectdb@sns.mysql.pythonanywhere-services.com/sns$stocks")
    connection = engine.connect()

    sql_query = pd.read_sql_query(''' 
                                  select Date, Ticker, Performance, Volume from snp_performance_2023_01_11 limit 5;
                                  '''
                                  ,
                                  connection)  # here, the 'conn' is the variable that contains your database connection information from step 2

    df = pd.DataFrame(sql_query)
    df.to_csv(r'exported_data.csv', index=False)  # place 'r' before the path name

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    export_snp('Export')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/