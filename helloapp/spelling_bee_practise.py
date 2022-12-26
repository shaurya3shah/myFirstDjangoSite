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
word_list_check=[]

print(items[0])

stop_flag=False

for current_word in items:
    if current_word["count_right"] == 0:
        print(current_word["word"])
        check = input("Was it spelled correctly [y/n/exit] : ")

        if check == "y":
            current_word["count_right"] = current_word["count_right"] + 1
        elif check == "n":
            current_word["count_wrong"] = current_word["count_wrong"] +1
        else:
            print("good bye")
            break

        word_list_check.append(current_word)

print("The practised word for today ")
for i in word_list_check:
    print(f" {i['word']} : count right is {i['count_right']} and  count wrong is {i['count_wrong']}")
    #Put the things in DB
    try:
        response = table.update_item( Key={"id": i["id"]},
                UpdateExpression="set count_right=:r, count_wrong=:w",
                ExpressionAttributeValues={":r": i["count_right"],":w": i["count_wrong"]},
                ReturnValues="UPDATED_NEW",
                )
    except Exception as err:
        print(err)
        raise



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
