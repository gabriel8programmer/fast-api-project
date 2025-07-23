
import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzUzODk5NjkxfQ.5HWlZ-PD-aTsg2_BErSVt3vQ_lO7hoUiF0aaEjJha2A'
}

request = requests.get('http://localhost:8000/auth/refresh', headers=headers)

print(request)
print(request.json())
