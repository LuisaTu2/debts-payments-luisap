import requests
import json
import sys
from urllib.parse import urljoin

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

def process_debts_payments():
	
	base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
	
	debts_url = urljoin(base_url, 'debts')
	payment_plans_url = urljoin(base_url, 'payment_plans')
	payments_url = urljoin(base_url, 'payments')

	#write_jsonl(response)
	debts = get_resource(debts_url)
	payment_plans = get_resource(payment_plans_url)
	payments = get_resource(payments_url)
	
	print('\n\nDEBTS')
	print(debts)
	print('\n\nPAYMENT PLANS')
	print(payment_plans)
	print('\n\nPAYMENTS')
	print(payments)
	print("\n\n****************************")
	
	res = [];
	
	if debts is not None:
		if payment_plans is not None:
			for debt in debts:
				payment_plan = [payment_plan for payment_plan in payment_plans if payment_plan['debt_id'] == debt['id']]
				print(debt, len(payment_plan))
				
		else:
			print('There are no payment plans')
				
			
	

process_debts_payments();


 

