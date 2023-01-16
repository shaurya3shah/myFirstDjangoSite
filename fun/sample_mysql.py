import sqlalchemy as db
import pandas as pd

engine = db.create_engine("mysql://root:Hello123!@localhost/playlearn")
connection = engine.connect()
result = connection.execute("select * from table_test;")

for row in result.fetchall():
    print(row)
#
# data = [10,20,30,40,50,60]
#
# df = pd.DataFrame(data, columns=['Numbers'])
#
# print(df)
#
# df.to_sql(name = 'pandas_table', con = engine, if_exists = 'append', index = True)
#
# result = connection.execute("select * from pandas_table;")
#
# for row in result.fetchall():
#     print(row)
