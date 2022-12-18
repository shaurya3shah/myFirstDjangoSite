import boto3
import os

client = boto3.client('dynamodb',aws_access_key_id = os.environ["KEY_ID"], aws_secret_access_key = os.environ["SECRET_ACCESS_KEY"])

dynamodb = boto3.resource('dynamodb',aws_access_key_id = os.environ["KEY_ID"],aws_secret_access_key = os.environ["SECRET_ACCESS_KEY"])

table_name = "Word_List"

table = dynamodb.Table(table_name)
response = table.scan()
print(response)

#for i in range(1,10):
#    response = table.get_item(Key={'id': i})
#    print(response["Item"])
#    for key in response["Item"]:
#        print(key,response["Item"][key])

