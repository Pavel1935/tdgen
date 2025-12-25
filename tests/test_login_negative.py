import json
import pytest
from pathlib import Path


def fake_login_api(payload):
    if "email" not in payload or "password" not in payload:
        return 400

    if not payload["email"].strip():
        return 400
    if not payload["password"].strip():
        return 400

    if len(payload["password"]) < 8:
        return 400

    return 400


BASE_DIR = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = BASE_DIR / "output" / "payload.json"

with open(PAYLOAD_PATH, encoding="utf-8") as f:
    payloads = json.load(f)


@pytest.mark.parametrize("payload", payloads)
def test_login_negative(payload):
    status_code = fake_login_api(payload)
    assert status_code == 400
