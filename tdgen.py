import argparse
import json
from pathlib import Path

def parse_args():
    """
    Читает аргументы командной строки.
    Например:
    --schema schemas/user.json
    --out output/payload.json
    """
    parser = argparse.ArgumentParser(description="Test Data Generator")

    # путь к файлу со схемой
    parser.add_argument(
        "--schema",
        required=True,
        help="Path to schema JSON file"
    )

    # куда сохраняю  результат
    parser.add_argument(
        "--out",
        default="output/payload.json",
        help="Output file path"
    )

    return parser.parse_args()

def generate_valid_value(field_schema):
    """
    генерируем валидное значение для ОДНОГО поля
    на основании его описания в схеме
    """

    # тип поля (email, string, int)
    field_type = field_schema["type"]

    
    if field_type == "email":
        # рандомный  email
        return "email@email.com"

    
    elif field_type == "string":
        # если min_length не указан  берём 1
        min_length = field_schema.get("min_length", 1)
        return "a" * min_length

    
    elif field_type == "int":
        # если min не указан  берём 0
        min_value = field_schema.get("min", 0)
        return min_value

    # неизвестный тип и раис исключение
    else:
        raise ValueError(f"Unsupported field type: {field_type}")

def generate_invalid_value(field_schema, rule):
    field_type = field_schema["type"]

    #EMAIL
    if field_type == "email" and rule == "invalid_format":
        return "email.email.com"

    elif field_type == "email" and rule == "empty":
        return ""

    elif field_type == "email" and rule == "missing":
        return None

    elif field_type == "email" and rule == "only_spaces":
        return "  "

    elif field_type == "email" and rule == "leading_trailing_spaces":
        return "  email@email.com  "

    elif field_type == "email" and rule == "too_long":
        return "a" * 256 + "@mail.com"

    # STRING
    elif field_type == "string" and rule == "shorter_than_min":
        min_length = field_schema.get("min_length", 1)
        return "a" * (min_length - 1)

    elif field_type == "string" and rule == "empty":
        return ""

    elif field_type == "string" and rule == "only_spaces":
        return "  "

    elif field_type == "string" and rule == "too_long":           
        return "a" * 1000 

def generate_payload(schema):
    """
    собирает один валидный payload на основании всей схемы.
    """

    payload = {}

    # schema  это словарь вида:
    # { "email": {...}, "password": {...} }
    for field_name, field_schema in schema.items():
        payload[field_name] = generate_valid_value(field_schema)

    return payload

def generate_invalid_payloads(schema, invalid_rules):
    payloads = []

    # базовый валидный payload
    base_payload = generate_payload(schema)

    # идём по всем полям схемы
    for field_name, field_schema in schema.items():
        field_type = field_schema["type"]

        # если для этого типа нет правил — пропускаем
        if field_type not in invalid_rules:
            continue

        rules = invalid_rules[field_type]

        for rule in rules:
            payload = base_payload.copy()
            invalid_value = generate_invalid_value(field_schema, rule)

            if rule == "missing":
                payload.pop(field_name, None)
            else:
                payload[field_name] = invalid_value

            payloads.append(payload)

    return payloads

def main():
    # читаем аргументы CLI
    args = parse_args()

    # читаем JSON-схему из файла
    schema_path = Path(args.schema)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    # читаем негативную JSON-схему из файла
    rules_path = Path("schemas/invalid_rules.json") 
    invalid_rules = json.loads(rules_path.read_text(encoding="utf-8"))

    # генерируем НЕВАЛИДНЫЕ payload'ы
    payloads = generate_invalid_payloads(schema, invalid_rules)

    # сохраняем результат в файл
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(
        json.dumps(payloads, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Payload saved to {out_path}")


if __name__ == "__main__":
    main()

