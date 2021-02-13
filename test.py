import unittest
from debts import get_resource
#from debts import process_debts_payments
from unittest.mock import patch
from unittest.mock import Mock

class TestDebtsPayments(unittest.TestCase):
	
	@patch('debts.requests.get')
	def test_get_resource_is_successful(self, mock_get):
		#base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
		resp_status_code = 200
		mock_get.return_value.status_code = resp_status_code
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertEqual(response.status_code, resp_status_code)
	
	@patch('debts.requests.get')	
	def test_get_resource_returns_none_when_response_not_200(self, mock_get):
		resp_status_code = 204
		mock_get.return_value.status_code = resp_status_code
		response = get_resource('')
		self.assertTrue(mock_get.called)
		#self.assertEqual(response.status_code, resp_status_code)
		self.assertIsNone(response)
	
	"""
	@patch('debts.requests.get')	
	def test_get_resource_returns_none_when_response_400(self, mock_get):
		resp_status_code = 400
		mock_get.return_value.status_code = resp_status_code
		#response = get_resource('')
		#self.assertTrue(mock_get.called)
		#self.assertEqual(response.status_code, resp_status_code)
		#self.assertIsNone(mock_get)
	"""		
	
		
if __name__ == '__main__':
	unittest.main()
