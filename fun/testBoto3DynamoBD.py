import unittest
from pprint import pprint

import boto3

from myFirstDjangoSite.settings import env
from decimal import Decimal
import time


class TestBoto3DynamoDBCase(unittest.TestCase):
    pass
#     dyn_resource = boto3.resource('dynamodb',
#                                   aws_access_key_id=env("KEY_ID"),
#                                   aws_secret_access_key=env("SECRET_ACCESS_KEY"),
#                                   region_name="us-west-2")
#     table_name = 'unit_test_table'
#
#     def test_table_create(self):
#         print("Creating table: " + self.table_name)
#         try:
#             table = self.dyn_resource.create_table(
#                 TableName=self.table_name,
#                 KeySchema=[
#                     {
#                         'AttributeName': 'timestamp',
#                         'KeyType': 'HASH'
#                     }
#                 ],
#                 AttributeDefinitions=[
#                     {
#                         'AttributeName': 'timestamp',
#                         'AttributeType': 'N'
#                     }
#                 ],
#                 ProvisionedThroughput={
#                     'ReadCapacityUnits': 10,
#                     'WriteCapacityUnits': 10
#                 }
#             )
#
#             waiter = self.dyn_resource.get_waiter('table_exists')
#             waiter.wait(TableName=self.table_name)
#             print("Table created: " + str(table))
#
#         except Exception as e:
#             print(self.table_name + " Table exists " + e.__str__())
#
#         self.assertEqual(True, True)  # add assertion here
#
#
#     def test_write_my_option(self):
#         my_option = MyOption()
#         table = self.dyn_resource.Table(self.table_name)
#         table.load()
#         response = table.put_item(
#             Item={
#                 'timestamp': Decimal(time.time()),
#                 'my_option': my_option.__dict__,
#             },
#         )
#         print(response)
#
#         items = table.scan()["Items"]
#         pprint(items)
#
#         self.assertEqual(True, True)  # add assertion here
#
#     def test_write_my_question(self):
#         my_question = MyQuestion()
#         table = self.dyn_resource.Table(self.table_name)
#         table.load()
#         response = table.put_item(
#             Item={
#                 'timestamp': Decimal(time.time()),
#                 'question_text': my_question.question_text,
#                 'option1': my_question.options['option1'].__dict__,
#                 'option2': my_question.options['option2'].__dict__,
#             },
#         )
#         print(response)
#
#         items = table.scan()["Items"]
#         pprint(items)
#
#         self.assertEqual(True, True)  # add assertion here
#
#     def test_read_table(self):
#         table = self.dyn_resource.Table(self.table_name)
#         items = table.scan()["Items"]
#         pprint(items)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
#
# class MyOption:
#     option_text = ''
#     score = {}
#
#     def __init__(self):
#         self.option_text = 'wow options!'
#         self.score = {'g_score': 1, 's_score': 2}
#
#
# class MyQuestion:
#     question_text = '?'
#     options = {}
#
#     def __init__(self):
#         self.question_text = 'why?'
#         option_1 = MyOption()
#         option_2 = MyOption()
#         self.options = {'option1': option_1, 'option2': option_2}
