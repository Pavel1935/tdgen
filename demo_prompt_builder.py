import requests

from prompt_builder import PromptBuilder


API_URL = "http://127.0.0.1:8000/users"

payload = {
    "email": "email@email.com",
    "password": "ValidPass123",
}

response = requests.post(API_URL, json=payload)

builder = PromptBuilder()
builder.add_endpoint("POST", API_URL)
builder.add_payload(payload)
builder.add_expected_status(400)

try:
    response_body = response.json()
except ValueError:
    response_body = response.text

builder.add_actual_response(response.status_code, response_body)

print(builder.build())

