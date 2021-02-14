import requests
import json
import sys
import copy
from urllib.parse import urljoin
import functools

# outputs a list of dictionaries to stdout in JSON LINES format 
def write_jsonl(items):
	for item in items:
		item_json = json.dumps(item)
		sys.stdout.write(item_json)
		sys.stdout.write('\n')
		
def get_resource(url):
	try:
		response = requests.get(url, verify=False, timeout=5)
		if response.status_code == 200:
			return response.json()
		else:
			return None
	except Exception as e:
		print(e)
		return None


def process_data(debts, payment_plans, payments):
	
	if debts is None or len(debts) <= 0:
		return None
		
	res = []
	
	for debt in debts:		
		d = copy.deepcopy(debt);
		print('\n\n\nDEBT: ', d)
		payment_plan = []
		if payment_plans is not None:
			payment_plan = [payment_plan for payment_plan in payment_plans if payment_plan['debt_id'] == debt['id']]
			is_in_payment_plan = len(payment_plan) > 0
			remaining_amount = None
			#print('PAYMENT PLAN: ', payment_plan)
			if payments is not None and is_in_payment_plan:
				payment_plan_id = payment_plan[0]['id']
				amount_to_pay = payment_plan[0]['amount_to_pay']
				print('PAYMENT PLAN ID: ', payment_plan_id)
				payments_on_debt = list(filter(lambda x: x['payment_plan_id'] == payment_plan_id, payments))
				#paid_amount = functools.reduce(lambda x, y: x['amount'] + y['amount'], payments_on_debt) # Float obj is not subscriptable
				paid_amount = sum([payment['amount'] for payment in payments_on_debt])			
				remaining_amount = amount_to_pay - paid_amount;
				#print("PAYMENTS MADE ON DEBT: ", payments_on_debt)
				#print("PAID AMOUNT: ", paid_amount)
				#print("REMAINING AMOUNT: ", remaining_amount)
				
				
			else:
				print('No payments were returned')
		else:
			print('No payment plans were returned')
		d['is_in_payment_plan'] = is_in_payment_plan
		d['remaining_amount'] = remaining_amount
		print(d)
		
		
		
		#r['remaining_amount'] = 0;
		#r['next_payment_due_date'] = 0;
		
		res.append(d)
		


	
def main():			
	base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'

	debts_url = urljoin(base_url, 'debts')
	payment_plans_url = urljoin(base_url, 'payment_plans')
	payments_url = urljoin(base_url, 'payments')

	debts = get_resource(debts_url)		
	payment_plans = get_resource(payment_plans_url)
	payments = get_resource(payments_url)
	
	process_data(debts, payment_plans, payments)
	
	#res = []
	#write_jsonl(res)
	
	
main()
 

