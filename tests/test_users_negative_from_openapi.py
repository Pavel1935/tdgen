import json
import sys
from pathlib import Path

import pytest
import requests
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))


from prompt_builder import PromptBuilder
import json
from pathlib import Path

import pytest
import requests
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[1]
PAYLOADS_PATH = BASE_DIR / "output" / "payload_from_openapi.json"
API_URL = "http://127.0.0.1:8000/users"


class ErrorResponse(BaseModel):
    error: str
    field: str
    message: str


with open(PAYLOADS_PATH, encoding="utf-8") as file:
    negative_payloads = json.load(file)


@pytest.mark.parametrize("payload", negative_payloads)
def test_create_user_negative_from_openapi(payload):
    response = requests.post(API_URL, json=payload)

    if response.status_code != 400:
         builder = PromptBuilder()
         builder.add_endpoint("POST", API_URL)
         builder.add_payload(payload)
         builder.add_expected_status(400)

         try:
             response_body = response.json()
         except ValueError:
             response_body = response.text

         builder.add_actual_response(response.status_code, response_body)

         pytest.fail(builder.build())


    error = ErrorResponse.model_validate(response.json())

    assert error.error == "validation_error"
    assert error.field is not None
    assert error.message

