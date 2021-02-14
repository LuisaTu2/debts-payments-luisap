import unittest
import requests
from debts import get_resource
#from debts import process_debts_payments
from unittest.mock import patch
from unittest.mock import Mock

class TestDebtsPayments(unittest.TestCase):
	
	@patch('debts.requests.get')
	def test_get_resource_is_successful_on_200_response(self, mock_get):
		resp_status_code = 200
		mock_get.return_value.status_code = resp_status_code
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertEqual(response.status_code, resp_status_code)
		self.assertIsNotNone(response)
		
	@patch('debts.requests.get')
	def test_get_resource_returns_none_on_204_response(self, mock_get):
		resp_status_code = 204
		mock_get.return_value.status_code = resp_status_code
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertIsNone(response)
	
	@patch('debts.requests.get')	
	def test_get_resource_returns_none_on_HTTP_error(self, mock_get):
		mock_get.side_effect = requests.HTTPError
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertIsNone(response)
		
	@patch('debts.requests.get')	
	def test_get_resource_returns_none_on_exception(self, mock_get):
		mock_get.side_effect = Exception('test exception')
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertIsNone(response)
	
	def test_get_resource_returns_not_none_on_valid_url(self):
		valid_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts'
		result = get_resource(valid_url)
		self.assertIsNotNone(result)
		
	def test_get_resource_returns_none_successful_on_invalid_url(self):
		invalid_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/det'
		result = get_resource(invalid_url)
		self.assertIsNone(result)
		
		
if __name__ == '__main__':
	unittest.main()
