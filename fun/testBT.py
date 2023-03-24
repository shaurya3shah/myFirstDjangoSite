import unittest

from python_graphql_client import GraphqlClient
from requests.auth import HTTPBasicAuth


class BTTestCase(unittest.TestCase):
    def test_basic_gql_connect(self):
        # Instantiate the client with an endpoint.
        client = GraphqlClient(endpoint="https://countries.trevorblades.com")

        # Create the query string and variables required for the request.
        query = """
            query countryQuery($countryCode: ID!) {
                country(code:$countryCode) {
                    code
                    name
                }
            }
        """

        variables = {"countryCode": "US"}

        # Synchronous request
        data = client.execute(query=query, variables=variables)
        print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

        self.assertEqual(True, True)  # add assertion here

    def test_bt_ping(self):
        # Instantiate the client with an endpoint.
        headers = {'Authorization': 'Basic cjV6NDNkdGQzdmo2amo1aDpjMjQ4NGRkZTYyZjhiMGZlNWNlYjQ1ZDc0YWQ0MmYyNA==',
                   'Braintree-Version': '2023-03-01', 'Content-Type': 'application/json'}
        client = GraphqlClient(endpoint="https://payments.sandbox.braintree-api.com/graphql", headers=headers)

        # Create the query string and variables required for the request.
        query = """
            query {
                ping
            }
        """

        # Synchronous request
        data = client.execute(query=query)
        print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

        self.assertEqual(True, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()
