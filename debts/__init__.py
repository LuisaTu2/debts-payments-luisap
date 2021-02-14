import requests
import json
import sys
import copy
import functools
from datetime import date, timedelta
import dateutil.parser
from urllib.parse import urljoin

base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
debts_url = urljoin(base_url, 'debts')
payment_plans_url = urljoin(base_url, 'payment_plans')
payments_url = urljoin(base_url, 'payments')
days_in_one_week = 7
days_in_two_weeks = 14

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
		#print("Exception: ", e)
		return None

def get_remaining_amount(payment_plan, payments):
	try:	
		amount_to_pay = payment_plan['amount_to_pay']
		paid_amount = sum([p['amount'] for p in payments])			
		remaining_amount = amount_to_pay - paid_amount;
		return remaining_amount
	except Exception as e:
		#print("Exception: ", e)
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
			# Get the payment plan for given debt if payment plan exists else return None
			payment_plan = next(iter([p for p in payment_plans if p['debt_id'] == debt['id']]), None)
			is_in_payment_plan = payment_plan is not None
			remaining_amount = None
			next_payment_due_date = None
			
			if payments is not None and is_in_payment_plan:
				payment_plan_id = payment_plan['id']
				payments_history = list(filter(lambda p: p['payment_plan_id'] == payment_plan_id, payments))				
				remaining_amount = get_remaining_amount(payment_plan, payments_history)
				
				# Calculate the dates with the assumption that all dates are provided in ISO UTC format without any timezone offset
				# otherwise can incur 'can't compare offset-naive and offset-aware datetimes' error
				days_to_add = days_in_one_week if (payment_plan['installment_frequency'] == 'WEEKLY')  else days_in_two_weeks			
				start_date = dateutil.parser.parse(payment_plan['start_date'])
				next_payment_due_date = start_date if remaining_amount > 0 else next_payment_due_date
				last_payment_date = dateutil.parser.parse(functools.reduce(lambda x, y: x if dateutil.parser.parse(x['date']) > dateutil.parser.parse(y['date']) else y, payments_history)['date'])
				while next_payment_due_date is not None and next_payment_due_date <= last_payment_date and remaining_amount > 0:
					next_payment_due_date = next_payment_due_date + timedelta(days = days_to_add) 
				print('START DATE ', start_date, type(last_payment_date))
				print('LAST PAYMENT DATE ', last_payment_date, type(last_payment_date))
				print('INSTALLMENT FREQUENCY: ', payment_plan['installment_frequency'])
				print('NEXT PAYMENT DUE DATE ', next_payment_due_date, type(next_payment_due_date))

		d['is_in_payment_plan'] = is_in_payment_plan
		d['remaining_amount'] = remaining_amount
		# still in UTC but not with Z format
		d['next_payment_due_date'] = None if next_payment_due_date is None else next_payment_due_date.isoformat()
		#print(d)
		res.append(d)
		
	return res
		
	
def main():			

	debts = get_resource(debts_url)		
	payment_plans = get_resource(payment_plans_url)
	payments = get_resource(payments_url)
	
	result = process_data(debts, payment_plans, payments)
	
	if result is not None:
		write_jsonl(result)
	
	
#main()
 

