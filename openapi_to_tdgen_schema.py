import json
from pathlib import Path


OPENAPI_PATH = Path("openapi.json")
OUTPUT_PATH = Path("schemas/user_from_openapi.json")


def convert_field(field_name, field_schema, required_fields):
    field_type = field_schema.get("type")
    field_format = field_schema.get("format")

    result = {
        "required": field_name in required_fields
    }

    if field_type == "string" and field_format == "email":
        result["type"] = "email"
    elif field_type == "string":
        result["type"] = "string"
    else:
        result["type"] = field_type

    if "minLength" in field_schema:
        result["min_length"] = field_schema["minLength"]

    if "maxLength" in field_schema:
        result["max_length"] = field_schema["maxLength"]

    return result


def main():
    with open(OPENAPI_PATH) as file:
        openapi = json.load(file)

    create_user_schema = openapi["components"]["schemas"]["CreateUserRequest"]

    properties = create_user_schema["properties"]
    required_fields = create_user_schema.get("required", [])

    tdgen_schema = {}

    for field_name, field_schema in properties.items():
        tdgen_schema[field_name] = convert_field(
            field_name,
            field_schema,
            required_fields,
        )

    with open(OUTPUT_PATH, "w") as file:
        json.dump(tdgen_schema, file, indent=2)

    print(f"Saved tdgen schema to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

