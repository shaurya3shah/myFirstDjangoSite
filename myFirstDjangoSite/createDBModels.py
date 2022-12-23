class DBModels:
    def createSimpleTimestampDB(self, table_name, client, ddb_exceptions):
        print("Creating table: " + table_name)
        try:
            table = client.create_table(
                TableName=table_name,
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

            waiter = client.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            print("Table created: " + str(table))

        except ddb_exceptions.ResourceInUseException:
            print(table_name + " Table exists")
