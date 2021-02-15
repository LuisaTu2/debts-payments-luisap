import requests
import json
import sys
import copy
import functools
import dateutil.parser
from datetime import date, timedelta
from urllib.parse import urljoin

base_url = 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/'
debts_url = urljoin(base_url, 'debts')
payment_plans_url = urljoin(base_url, 'payment_plans')
payments_url = urljoin(base_url, 'payments')
days_in_one_week = 7
days_in_two_weeks = 14

# Outputs a list of dictionaries to stdout in JSON LINES format 
def write_jsonl(items):
	try:	
		for item in items:
			item_json = json.dumps(item)
			sys.stdout.write(item_json)
			sys.stdout.write('\n')
	except Exception as e:
		return
		
def get_resource(url):
	try:
		response = requests.get(url, verify=False, timeout=5)
		if response.status_code == 200:
			return response.json()
		else:
			return None
	except Exception as e:
		return None

def get_remaining_amount(payment_plan, payments):
	try:	
		amount_to_pay = payment_plan['amount_to_pay']
		paid_amount = sum([p['amount'] for p in payments])			
		remaining_amount = amount_to_pay - paid_amount;
		return remaining_amount
	except Exception as e:
		return None

# NOTE : dates are calculated with the assumption that all are provided in same format. 
# Discrepancies can cause errors when comparing offset-naive and offset-aware datetimes 
def get_next_payment_due_date(remaining_amount, payment_plan, payments):	
	try:
		days_between_installments = days_in_one_week if (payment_plan['installment_frequency'] == 'WEEKLY')  else days_in_two_weeks			
		start_date = dateutil.parser.parse(payment_plan['start_date'])
		next_payment_due_date = start_date if remaining_amount > 0 else None
		get_latest_payment_date = lambda x, y: x if dateutil.parser.parse(x['date']) > dateutil.parser.parse(y['date']) else y
		last_payment_date = dateutil.parser.parse(functools.reduce(get_latest_payment_date, payments)['date'])
		while next_payment_due_date is not None and next_payment_due_date <= last_payment_date and remaining_amount > 0:
			next_payment_due_date = next_payment_due_date + timedelta(days = days_between_installments) 
		return next_payment_due_date
	except Exception as e:
		return None

def handler(debts, payment_plans, payments):
	
	if debts is None or len(debts) <= 0:
		return None		
	res = []	
	try:
		for debt in debts:		
			d = copy.deepcopy(debt);
			is_in_payment_plan = None
			remaining_amount = None
			next_payment_due_date = None
			
			if payment_plans is not None:
				# Get the payment plan for given debt if exists else return None
				payment_plan = next(iter([p for p in payment_plans if p['debt_id'] == debt['id']]), None)
				is_in_payment_plan = payment_plan is not None
				
				if payments is not None and is_in_payment_plan:
					payment_plan_id = payment_plan['id']
					payments_history = list(filter(lambda p: p['payment_plan_id'] == payment_plan_id, payments))				
					remaining_amount = get_remaining_amount(payment_plan, payments_history)
					next_payment_due_date = get_next_payment_due_date(remaining_amount, payment_plan, payments_history)

			d['is_in_payment_plan'] = is_in_payment_plan
			d['remaining_amount'] = remaining_amount
			d['next_payment_due_date'] = None if next_payment_due_date is None else next_payment_due_date.isoformat()
			res.append(d)
			
		return res
	
	except Exception as e:
		return None		

	
def main():			
	debts = get_resource(debts_url)		
	payment_plans = get_resource(payment_plans_url)
	payments = get_resource(payments_url)
	result = handler(debts, payment_plans, payments)
	if result is not None:
		write_jsonl(result)
	 
if __name__ == '__main__':
	main()
