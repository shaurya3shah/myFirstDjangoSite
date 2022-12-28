import boto3
import os
import pandas
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# aws_access_key_id=os.environ["KEY_ID"]
# aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"]

# engine = create_engine("amazondynamodb:///?Access Key=${aws_access_key_id}&Secret Key=${aws_secret_access_key}&Domain=amazonaws.com&Region=OREGON")
# df = pandas.read_sql("SELECT id,word,count_right,count_Wrong FROM Word_List", engine)

# df.plot(kind="bar", x="word", y="count_right")
# plt.show()

def dynamo_db_to_list():
    client = boto3.client(
        "dynamodb",
        aws_access_key_id=os.environ["KEY_ID"],
        aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
    )

    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ["KEY_ID"],
        aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
    )

    table_name = "Word_List"

    table = dynamodb.Table(table_name)
    items = table.scan()["Items"]
    return items
