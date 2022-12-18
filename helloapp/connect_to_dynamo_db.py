import boto3

from myFirstDjangoSite.settings import env

client = boto3.client(
    'dynamodb',
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=env("KEY_ID"),
    aws_secret_access_key=env("SECRET_ACCESS_KEY"),
    region_name="us-west-2"
)
ddb_exceptions = client.exceptions

try:
    table = client.create_table(
        TableName='ISS_locations',
        KeySchema=[
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Creating table")
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName='ISS_locations')
    print("Table created")

except ddb_exceptions.ResourceInUseException:
    print("Table exists")

table_name = "ISS_locations"
response = client.put_item(
    TableName=table_name,
    Item={
        "timestamp": {"N": "1"},
        "order_id": {"S": "ord1234"},
        "order_date": {"S": "2022-08-03"},
        "user_email": {"S": "test@example.com"},
        "amount": {"N": "120"},
    },
)
print(response)
