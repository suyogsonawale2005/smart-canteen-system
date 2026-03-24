import requests
import json

payload = {
    "customer_id": 1,
    "items": [
        {"item_id": 1, "quantity": 1, "price": 20.0}
    ]
}

res = requests.post('https://smart-canteen-system-hvah.onrender.com/api/orders', json=payload)
print("Status Code:", res.status_code)
print("Response:", res.text)
