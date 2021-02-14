import unittest
import requests
from debts import main
from debts import get_resource
from debts import get_remaining_amount
from debts import process_data
from unittest.mock import patch
from unittest.mock import Mock, MagicMock

class TestDebtsPayments(unittest.TestCase):
	
	@patch('debts.get_resource')
	def test_main_calls_get_resource(self, mock_get_resource):
		main()
		self.assertTrue(mock_get_resource.called)
		self.assertTrue(mock_get_resource.call_count, 3)
		
	def test_get_remaining_amount_returns_valid_float(self):
		amount_to_pay = 100
		p1 = 30.0
		p2 = 22.6
		test_payment_plan = {'amount_to_pay' : amount_to_pay}
		test_payment_1 = { 'amount' : p1 }
		test_payment_2 = { 'amount' : p2 }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_remaining_amount(test_payment_plan, test_payments)
		self.assertIsNotNone(res)
		self.assertEqual(res, amount_to_pay - p1 - p2)
		
	def test_get_remaining_amount_returns_none_on_invalid_payment_plan(self):
		p1 = 30.0
		p2 = 22.6
		test_payment_plan = {}
		test_payment_1 = { 'amount' : p1 }
		test_payment_2 = { 'amount' : p2 }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_remaining_amount(test_payment_plan, test_payments)
		self.assertIsNone(res)
		
	def test_get_remaining_amount_returns_none_on_invalid_payment(self):
		amount_to_pay = 100
		p2 = 22.6
		test_payment_plan = {'amount_to_pay' : amount_to_pay}
		test_payment_1 = {}
		test_payment_2 = { 'amount' : p2 }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_remaining_amount(test_payment_plan, test_payments)
		self.assertIsNone(res)
		
	@patch('debts.process_data')
	def test_main_calls_process_data(self, mock_process_data):
		response = main()
		self.assertTrue(mock_process_data.called)
		
	def test_process_data_returns_none_on_none_or_empty_debts(self):
		res1 = process_data(None, Mock(), Mock())
		self.assertIsNone(res1)
		res2 = process_data([], Mock(), Mock())
		self.assertIsNone(res2)
		
	
	@patch('requests.get')
	def test_get_resource_is_successful_on_200_response(self, mock_get):
		mock_get.return_value.status_code = 200
		response = get_resource('')
		self.assertTrue(mock_get.called)
		#self.assertEqual(response.status_code, resp_status_code)
		self.assertIsNotNone(response)
		
	@patch('requests.get')
	def test_get_resource_returns_none_on_204_response(self, mock_get):
		resp_status_code = 204
		mock_get.return_value.status_code = resp_status_code
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertIsNone(response)
	
	@patch('requests.get')	
	def test_get_resource_returns_none_on_HTTP_error(self, mock_get):
		mock_get.side_effect = requests.HTTPError
		response = get_resource('')
		self.assertTrue(mock_get.called)
		self.assertIsNone(response)
		
	@patch('requests.get')	
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
