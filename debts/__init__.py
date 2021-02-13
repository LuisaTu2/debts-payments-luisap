import requests
import json
import sys
from urllib.parse import urljoin

'''
def sum(arg):
	total = 0 
	for val in arg:
		total += val
	return total
'''

# outputs a list of dictionaries to stdout in JSON LINES format 
def write_jsonl(items):
	for item in items:
		item_json = json.dumps(item)
		sys.stdout.write(item_json)
		sys.stdout.write("\n")
		
def get_resource(url):
	try:
		response = requests.get(url, verify=False, timeout=5).json()
		write_jsonl(response)
		return response
	except requests.exceptions.RequestException as e: #Check this
		#raise Exception("Request from ", url, " failed.");
		print("Something went wrong")
		raise SystemExit(e)

def process_debts_payments():
	
	base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
	
	debts_url = urljoin(base_url, 'debts')
	payment_plans_url = urljoin(base_url, 'payment_plans')
	payments_url = urljoin(base_url, 'payments')

	print("\n\nDEBTS")
	debts = get_resource(debts_url)
	print("\n\nPAYMENT PLANS")
	payment_plans = get_resource(payment_plans_url)
	print("\n\nPAYMENTS")
	payments = get_resource(payments_url)

process_debts_payments();


 

