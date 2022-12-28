import boto3
import os
import datetime

def get_single_item(item_key):
    response = table.get_item(Key=item_key)
    return response

client = boto3.client(
    'dynamodb',
 aws_access_key_id = os.environ["KEY_ID"], aws_secret_access_key = os.environ["SECRET_ACCESS_KEY"]
    )
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = os.environ["KEY_ID"],
    aws_secret_access_key = os.environ["SECRET_ACCESS_KEY"]
    )
ddb_exceptions = client.exceptions

try:
    table = client.create_table(
        TableName='Word_List',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'N'},
        ],
        ProvisionedThroughput={
                               'ReadCapacityUnits': 10,
                                           'WriteCapacityUnits': 10
                                           }

    )
    print("Creating table")
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName='Word_List')
    print("Table created")

except ddb_exceptions.ResourceInUseException:
    print("Table exists")

table_name = "Word_List"

#Get the table value from  a file
word_file=open("spelling.txt", "r")

for i in word_file.readlines():
    i = i.rstrip("\n")
    field=i.split(',')
    print(field[0])

    print(field[1])
    print(field[2])
    print(field[3])
    response = client.put_item(
            TableName=table_name,
            Item={
                "id" : {"N": field[0] },
                "word" : {"S" : field[1]},
                "count_wrong" : {"N" : field[2] },
                "count_right" : {"N" : field[3] },
    },
   )
    print(response)

table = dynamodb.Table(table_name)
item_key = { "id" : "1"}
response = table.get_item(Key={'id': 1})
print(response["Item"])

