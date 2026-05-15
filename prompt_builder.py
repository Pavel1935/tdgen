import json


class PromptBuilder:
    def __init__(self):
        self.parts = []

    def add_endpoint(self, method: str, url: str):
        self.parts.append(f"ENDPOINT:\n{method} {url}")

    def add_payload(self, payload: dict):
        formatted_payload = json.dumps(payload, indent=2, ensure_ascii=False)
        self.parts.append(f"PAYLOAD:\n{formatted_payload}")

    def add_expected_status(self, status_code: int):
        self.parts.append(f"EXPECTED STATUS:\n{status_code}")

    def add_actual_response(self, status_code: int, body: dict | str):
        if isinstance(body, dict):
            body = json.dumps(body, indent=2, ensure_ascii=False)

        self.parts.append(
            f"ACTUAL RESPONSE:\nStatus: {status_code}\nBody:\n{body}"
        )

    def build(self) -> str:
        return (
    "Ты QA Automation Engineer.\n"
    "Проанализируй падение негативного API-теста.\n"
    "Ответь на русском языке, коротко и по делу.\n\n"
    "Верни:\n"
    "1. Наиболее вероятная root cause\n"
    "2. Evidence из payload и response\n"
    "3. Тип проблемы: ошибка теста, ошибка API-валидации или неясно\n"
    "4. Suggested fix\n\n"
    + "\n\n".join(self.parts)
)

