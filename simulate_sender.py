import requests
import random
import time

recipients = ['123456', '888888', '999999']  # some fake accounts
while True:
    data = {
        'recipient': random.choice(recipients),
        'amount': random.randint(1000, 100000),
        'description': 'Auto Transaction'
    }
    res = requests.post('http://127.0.0.1:8000/api/receive-txn/', json=data)
    print(res.json())
    time.sleep(5)  # send every 5 seconds
