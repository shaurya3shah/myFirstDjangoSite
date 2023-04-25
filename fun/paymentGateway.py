from python_graphql_client import GraphqlClient


class PymentGateway:
    headers = {'Authorization': 'Basic cjV6NDNkdGQzdmo2amo1aDpjMjQ4NGRkZTYyZjhiMGZlNWNlYjQ1ZDc0YWQ0MmYyNA==',
               'Braintree-Version': '2023-03-01', 'Content-Type': 'application/json'}
    client = GraphqlClient(endpoint="https://payments.sandbox.braintree-api.com/graphql", headers=headers)

    # Create the query string and variables required for the request.
    query = """
                  mutation chargePaymentMethod($input: ChargePaymentMethodInput!) {
                      chargePaymentMethod(input: $input) {
                        transaction {
                          id
                          status
                        }
                      }
                    } 
            """

    def chargePaymentMethod(self, nonce):
        nonce = "fake-valid-visa-nonce"
        transaction = {"amount": "11.23"}
        input = {"paymentMethodId": nonce, "transaction": transaction}

        variables = {"input": input}

        # Synchronous request
        data = self.client.execute(query=self.query, variables=variables)
        print(data)

        return data

