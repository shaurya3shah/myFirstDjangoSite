import boto3
client = boto3.client(
    'dynamodb',
 aws_access_key_id = 'AKIAUW7UH47QX7CE35XH', aws_secret_access_key = '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'
    )
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = 'AKIAUW7UH47QX7CE35XH',
    aws_secret_access_key = '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'
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

