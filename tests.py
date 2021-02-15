import unittest
import requests
import datetime
from main import main
from main import get_resource
from main import handler
from main import get_remaining_amount
from main import get_next_payment_due_date
from unittest.mock import patch
from unittest.mock import Mock

class TestDebtsPayments(unittest.TestCase):
	
	# MAIN 
	@patch('main.get_resource')
	def test_main_calls_get_resource(self, mock_get_resource):
		main()
		self.assertTrue(mock_get_resource.called)
		self.assertTrue(mock_get_resource.call_count, 3)
		
	@patch('main.handler')
	def test_main_calls_get_resource(self, mock_handler):
		main()
		self.assertTrue(mock_handler.called)
		self.assertTrue(mock_handler.call_count, 1)
	
	# GET_RESOURCE
	def test_get_resource_returns_not_none_on_valid_url(self):
		valid_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts'
		result = get_resource(valid_url)
		self.assertIsNotNone(result)
		
	def test_get_resource_returns_none_successful_on_invalid_url(self):
		invalid_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/det'
		result = get_resource(invalid_url)
		self.assertIsNone(result)
	
	# GET_REMAINING_AMOUNT 
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
		self.assertAlmostEqual(res, amount_to_pay - p1 - p2)
		
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
	
	
	# GET_NEXT_PAYMENT_DUE_DATE 
	def test_get_next_payment_due_date_returns_valid_date(self):
		test_remaining_amount = 500
		test_payment_plan = { 'installment_frequency': 'WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_1 = { 'date' : '2020-09-28T16:18:30Z' }
		test_payment_2 = { 'date' : '2020-09-29T17:19:31Z' }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_next_payment_due_date(test_remaining_amount, test_payment_plan, test_payments)
		self.assertIsNotNone(res)
		
	def test_get_next_payment_due_date_returns_none_on_no_remaining_amount(self):
		test_remaining_amount = 0
		test_payment_plan = { 'installment_frequency': 'WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_1 = { 'date' : '2020-09-28T16:18:30Z' }
		test_payment_2 = { 'date' : '2020-09-29T17:19:31Z' }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_next_payment_due_date(test_remaining_amount, test_payment_plan, test_payments)
		self.assertIsNone(None)
		
	def test_get_next_payment_due_date_returns_none_on_invalid_payment_plan(self):
		test_remaining_amount = 100
		test_payment_plan = { 'installment_frequency': 'WEEKLY' }
		test_payment_1 = { 'date' : '2020-09-28T16:18:30Z' }
		test_payment_2 = { 'date' : '2020-09-29T17:19:31Z' }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_next_payment_due_date(test_remaining_amount, test_payment_plan, test_payments)
		self.assertIsNone(None)
		
	def test_get_next_payment_due_date_returns_none_on_invalid_payment(self):
		test_remaining_amount = 100
		test_payment_plan = { 'installment_frequency': 'WEEKLY', 'start_date' : '2020-09-01T16:18:30Z' }
		test_payment_1 = { }
		test_payment_2 = { 'date' : '2020-09-29T17:19:31Z' }
		test_payments = [ test_payment_1, test_payment_2 ]
		res = get_next_payment_due_date(test_remaining_amount, test_payment_plan, test_payments)
		self.assertIsNone(None)
	
	
	# HANDLER		
	def test_handler_returns_none_on_empty_debts(self):
		res1 = handler(None, Mock(), Mock())
		self.assertIsNone(res1)
		res2 = handler([], Mock(), Mock())
		self.assertIsNone(res2)
		
	def test_handler_returns_valid_response(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'id' : 2, 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plan_1 = { 'id' : 0, 'debt_id': 0, 'amount_to_pay': 200.77, 'installment_amount': 10, 'installment_frequency': 'BI-WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_plan_2 = { 'id' : 1, 'debt_id': 1, 'amount_to_pay': 99.66, 'installment_amount': 5.123, 'installment_frequency': 'WEEKLY', 'start_date' : '2020-03-01T16:18:30Z'  }
		test_payment_plans = [ test_payment_plan_1, test_payment_plan_2 ]
		test_payments = [ { 'amount' : 15, 'date': '2020-09-21T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 45, 'date': '2020-09-22T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 15, 'date': '2020-04-21T16:18:30Z', 'payment_plan_id': 1 } ]
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNotNone(res)
	
	def test_handler_returns_valid_response_null_payment_plans(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'id' : 2, 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plans = None
		test_payments = [ { 'amount' : 15, 'date': '2020-09-21T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 45, 'date': '2020-09-22T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 15, 'date': '2020-04-21T16:18:30Z', 'payment_plan_id': 1 } ]
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNotNone(res)
	
	def test_handler_returns_valid_response_null_payments(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'id' : 2, 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plan_1 = { 'id' : 0, 'debt_id': 0, 'amount_to_pay': 200.77, 'installment_amount': 10, 'installment_frequency': 'BI-WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_plan_2 = { 'id' : 1, 'debt_id': 1, 'amount_to_pay': 99.66, 'installment_amount': 5.123, 'installment_frequency': 'WEEKLY', 'start_date' : '2020-03-01T16:18:30Z'  }
		test_payment_plans = [ test_payment_plan_1, test_payment_plan_2 ]
		test_payments = None
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNotNone(res)
		
	def test_handler_returns_none_on_invalid_input_debt_id_in_debts(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plan_1 = { 'id' : 0, 'amount_to_pay': 200.77, 'installment_amount': 10, 'installment_frequency': 'BI-WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_plan_2 = { 'id' : 1, 'debt_id': 1, 'amount_to_pay': 99.66, 'installment_amount': 5.123, 'installment_frequency': 'WEEKLY', 'start_date' : '2020-03-01T16:18:30Z'  }
		test_payment_plans = [ test_payment_plan_1, test_payment_plan_2 ]
		test_payments = [ { 'amount' : 15, 'date': '2020-09-21T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 45, 'date': '2020-09-22T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 15, 'date': '2020-04-21T16:18:30Z', 'payment_plan_id': 1 } ]
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNone(res)
		
	def test_handler_returns_none_on_invalid_input_debt_id_in_payment_plans(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'id' : 2, 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plan_1 = { 'id' : 0, 'amount_to_pay': 200.77, 'installment_amount': 10, 'installment_frequency': 'BI-WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_plan_2 = { 'id' : 1, 'debt_id': 1, 'amount_to_pay': 99.66, 'installment_amount': 5.123, 'installment_frequency': 'WEEKLY', 'start_date' : '2020-03-01T16:18:30Z'  }
		test_payment_plans = [ test_payment_plan_1, test_payment_plan_2 ]
		test_payments = [ { 'amount' : 15, 'date': '2020-09-21T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 45, 'date': '2020-09-22T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 15, 'date': '2020-04-21T16:18:30Z', 'payment_plan_id': 1 } ]
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNone(res)
	
	def test_handler_returns_none_on_invalid_payment_plan_id_in_payments(self):
		test_debt_1 = { 'id' : 0, 'amount': 500.55 }
		test_debt_2 = { 'id' : 1, 'amount': 123.455 }	
		test_debt_3 = { 'id' : 2, 'amount': 21.55 }	
		test_debts = [ test_debt_1, test_debt_2, test_debt_3]
		test_payment_plan_1 = { 'id' : 0, 'debt_id': 0, 'amount_to_pay': 200.77, 'installment_amount': 10, 'installment_frequency': 'BI-WEEKLY', 'start_date' : '2020-09-01T16:18:30Z'  }
		test_payment_plan_2 = { 'id' : 1, 'debt_id': 1, 'amount_to_pay': 99.66, 'installment_amount': 5.123, 'installment_frequency': 'WEEKLY', 'start_date' : '2020-03-01T16:18:30Z'  }
		test_payment_plans = [ test_payment_plan_1, test_payment_plan_2 ]
		test_payments = [ { 'amount' : 15, 'date': '2020-09-21T16:18:30Z'}, { 'amount' : 45, 'date': '2020-09-22T16:18:30Z', 'payment_plan_id': 0 }, { 'amount' : 15, 'date': '2020-04-21T16:18:30Z', 'payment_plan_id': 1 } ]
		res = handler(test_debts, test_payment_plans, test_payments)
		self.assertIsNone(res)
	
	# GET REQUESTS	
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

		
if __name__ == '__main__':
	unittest.main()
