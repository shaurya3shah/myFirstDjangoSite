import time

from myFirstDjangoSite.settings import ddb_exceptions, client, dynamodb


class GuessNumber:
    guess_number_table_name = 'GuessNumber'

    def addResult(self, user_id, tries):
        try:
            response = client.put_item(
                TableName=self.guess_number_table_name,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "user_id": {"N": str(user_id)},
                    "tries": {"N": str(tries)}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))

    def getStats(self):
        response = dynamodb.Table(self.guess_number_table_name).scan()
        print(response)
        return response.get('Items')
