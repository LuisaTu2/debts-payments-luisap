import requests
import json
import sys
import copy
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


def process_data(debts, payment_plans, payments):
	
	if debts is None or len(debts) <= 0:
		return None
		
	res = []
	
	for debt in debts:		
		r = copy.deepcopy(debt);
		payment_plan = []
		if payment_plans is not None:
			payment_plan = [payment_plan for payment_plan in payment_plans if payment_plan['debt_id'] == debt['id']]
		r['is_in_payment_plan'] = len(payment_plan) > 0
		res.append(r)
		#r['remaining_amount'] = 0;
		#r['next_payment_due_date'] = 0;


	
def main():			
	base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'

	debts_url = urljoin(base_url, 'debts')
	payment_plans_url = urljoin(base_url, 'payment_plans')
	payments_url = urljoin(base_url, 'payments')

	debts = get_resource(debts_url)		
	payment_plans = get_resource(payment_plans_url)
	payments = get_resource(payments_url)
	
	process_data(debts, payment_plans, payments)
	res = []
	write_jsonl(res)
	
	
main()
 

