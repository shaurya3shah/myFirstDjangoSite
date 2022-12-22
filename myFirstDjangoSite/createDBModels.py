
class DBModels:
    def createGuessNumberDB(self, client, ddb_exceptions):
        guess_number_table_name = 'GuessNumber'
        print("Creating table" + guess_number_table_name)
        try:
            table = client.create_table(
                TableName=guess_number_table_name,
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
            waiter.wait(TableName=guess_number_table_name)
            print("Table created" + str(table))

        except ddb_exceptions.ResourceInUseException:
            print(guess_number_table_name + " Table exists")
