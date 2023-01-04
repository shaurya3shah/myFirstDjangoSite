from myFirstDjangoSite.constants import TABLE_NAME_FEEDBACK
from myFirstDjangoSite.settings import client, ddb_exceptions

import time


class Feedback:
    def addFeedback(self, user_id, feedback, email):
        try:
            response = client.put_item(
                TableName=TABLE_NAME_FEEDBACK,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "user_id": {"N": str(user_id)},
                    "feedback": {"S": str(feedback)},
                    "email": {"S": str(email)}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))