import boto3
import os
import pandas
import matplotlib.pyplot as plt
# from sqlalchemy import create_engine

from myFirstDjangoSite.settings import env

#aws_access_key_id=os.environ["KEY_ID"]
#aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"]

#engine = create_engine("amazondynamodb:///?Access Key=${aws_access_key_id}&Secret Key=${aws_secret_access_key}&Domain=amazonaws.com&Region=OREGON")
#df = pandas.read_sql("SELECT id,word,count_right,count_Wrong FROM Word_List", engine)

#df.plot(kind="bar", x="word", y="count_right")
#plt.show()


client = boto3.client(
    "dynamodb",
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)

table_name = "Word_List"

table = dynamodb.Table(table_name)
items = table.scan()["Items"]
#word_list_check=[]

df=pandas.DataFrame.from_dict(items)
print(df['id'])

df['id'] = pandas.to_numeric(df['id'])
df['count_right'] = pandas.to_numeric(df['count_right'])
df.plot(x='id', y='count_right')
print(plt.show())


#print(items[0])
