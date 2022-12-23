import time

from myFirstDjangoSite.constants import TABLE_NAME_GUESS_NUMBER
from myFirstDjangoSite.settings import ddb_exceptions, client, dynamodb


class GuessNumber:

    def addResult(self, user_id, tries):
        try:
            response = client.put_item(
                TableName=TABLE_NAME_GUESS_NUMBER,
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
        response = dynamodb.Table(TABLE_NAME_GUESS_NUMBER).scan()
        print(response)
        return response.get('Items')
