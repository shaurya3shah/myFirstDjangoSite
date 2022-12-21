import boto3
import os

client = boto3.client(
    "dynamodb",
    aws_access_key_id=os.environ["KEY_ID"],
    aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
)

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.environ["KEY_ID"],
    aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
)

table_name = "Word_List"

table = dynamodb.Table(table_name)
items = table.scan()["Items"]

print(items[0])

for word_dict in items:
    if word_dict["count_right"] == 0:
        print(word_dict["word"])
        check = input("Was it spelled correctly [y/n/exit] : ")

        if check == "y":
            count_right = word_dict["count_right"] + 1
            try:
                response = table.update_item(
                    Key={"id": word_dict["id"]},
                    UpdateExpression="set count_right=:r",
                    ExpressionAttributeValues={":r": count_right},
                    ReturnValues="UPDATED_NEW",
                )
            except Exception as err:
                print(err)
                raise
            else:
                print(response["Attributes"])



#        else:
#            word_dict["count_wrong"] = word_dict["count_wrong"] +1

# irint(items[0]["word"])

# for item in items:
#    print(item)
#    for k, v in item.items():
#        print(v)

# response = table.scan()
# print(response)

# for i in range(1,10):
#    response = table.get_item(Key={'id': i})
#    print(response["Item"])
#    for key in response["Item"]:
#        print(key,response["Item"][key])
