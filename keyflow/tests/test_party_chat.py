import json
import requests

from keyflow.tests.keyflow_parties_test_base import KeyflowPartiesTestBase


class TestAPIReadOperations(KeyflowPartiesTestBase):
    """
    Will show you how to read write on teh API, use a factory method for
    creating parties later.
    """

    def test_r(self):
      url = 'http://localhost:8080/v1/parties/1/chats/'
      post_body = {'message': 'hi'}
      auth_header = {"Authorization": "6"}
      response = requests.post(url, data=json.dumps(post_body), headers=auth_header)

      self.assertEqual(200, response.status_code)
