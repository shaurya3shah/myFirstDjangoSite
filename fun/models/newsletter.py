from myFirstDjangoSite.constants import TABLE_NAME_NEWSLETTER
from myFirstDjangoSite.settings import client, ddb_exceptions

import time

class Newsletter:
    def addNewsletterSignUp(self, email):
        try:
            response = client.put_item(
                TableName=TABLE_NAME_NEWSLETTER,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "email": {"S": str(email)}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))