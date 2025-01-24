import time

from myFirstDjangoSite.constants import TABLE_NAME_GUESS_NUMBER
from myFirstDjangoSite.settings import ddb_exceptions, client, dynamodb


class GuessNumber:
    guessed_number = int
    comparison = str
    secret_number = int
    guesses = []

    def addResult(self, user_id):
        try:
            response = client.put_item(
                TableName=TABLE_NAME_GUESS_NUMBER,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "user_id": {"N": str(user_id)},
                    "secret_number": {"N": str(self.secret_number)},
                    "guesses": {"S": str(self.guesses)},
                    "tries": {"N": str(len(self.guesses))}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))

    def getStats(self):
        response = dynamodb.Table(TABLE_NAME_GUESS_NUMBER).scan()
        print(response)
        return response.get('Items')

    def __init__(self):
        self.guesses = []

    def __str__(self):
        return str(self.guessed_number) + ' is ' + str(self.comparison) + ' than the secret number'
