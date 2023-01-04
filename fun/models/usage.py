from myFirstDjangoSite.constants import TABLE_NAME_USAGE
from myFirstDjangoSite.settings import client, ddb_exceptions, dynamodb

import time

class Usage:

    def saveUsage(self, REMOTE_ADDR, HTTP_HOST, HTTP_USER_AGENT, HTTP_X_REAL_IP, HTTP_X_FORWARDED_FOR):
        print(' REMOTE_ADDR: ' + REMOTE_ADDR + ' HTTP_HOST: ' + HTTP_HOST + ' HTTP_USER_AGENT: ' + HTTP_USER_AGENT
              + ' HTTP_X_REAL_IP: ' + HTTP_X_REAL_IP + ' HTTP_X_FORWARDED_FOR: ' + HTTP_X_FORWARDED_FOR)
        try:
            response = client.put_item(
                TableName=TABLE_NAME_USAGE,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "REMOTE_ADDR": {"S": str(REMOTE_ADDR)},
                    "HTTP_HOST": {"S": str(HTTP_HOST)},
                    "HTTP_USER_AGENT": {"S": str(HTTP_USER_AGENT)},
                    "HTTP_X_REAL_IP": {"S": str(HTTP_X_REAL_IP)},
                    "HTTP_X_FORWARDED_FOR": {"S": str(HTTP_X_FORWARDED_FOR)}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))
