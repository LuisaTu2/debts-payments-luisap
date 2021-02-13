import unittest
from debts import get_resource
#from debts import process_debts_payments

class TestSum(unittest.TestCase):
	
	def test_get_resource_is_successful(self):
		base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
		urls = [base_url + 'debts', base_url + 'payment_plans', base_url + 'payments']			
		
	#def test_process_debts_payments(self):
	#	testDebts = get_debts();
	#	self.assertEqual(testDebts[0].status_code, 200);
	
	#def test_is_JSON_line(self):
	#	data = [1,2,3];
	#	result = sum(data);
	#	self.assertEqual(result, 6, "Should be 6");
	
		
if __name__ == '__main__':
	unittest.main()
