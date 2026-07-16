#!/usr/bin/env python3
"""Validate schema/example-charges.json against schema/charges.schema.json.

No external dependencies. Run this first, right after cloning, before
trusting SubReaper with your own inbox:

    python3 test/validate_schema.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "charges.schema.json"
EXAMPLE_PATH = ROOT / "schema" / "example-charges.json"

_TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def _check_type(value, json_types):
    if isinstance(json_types, str):
        json_types = [json_types]
    py_types = tuple(_TYPE_MAP[t] for t in json_types)
    if isinstance(value, bool) and bool not in py_types:
        return False
    return isinstance(value, py_types)


def validate(schema, data):
    errors = []
    if schema.get("type") != "array":
        return [f"schema root: expected type 'array', got {schema.get('type')!r}"]
    if not isinstance(data, list):
        return [f"root: expected a JSON array, got {type(data).__name__}"]

    item_schema = schema["items"]
    required = item_schema.get("required", [])
    props = item_schema.get("properties", {})

    for i, item in enumerate(data):
        label = item.get("id", f"index {i}")
        for field in required:
            if field not in item:
                errors.append(f"{label}: missing required field '{field}'")
        for field, value in item.items():
            prop_schema = props.get(field)
            if prop_schema is None:
                continue
            if "type" in prop_schema and not _check_type(value, prop_schema["type"]):
                errors.append(
                    f"{label}: field '{field}' expected type {prop_schema['type']}, "
                    f"got {type(value).__name__}"
                )
            if "enum" in prop_schema and value not in prop_schema["enum"]:
                errors.append(
                    f"{label}: field '{field}' value {value!r} not in allowed "
                    f"values {prop_schema['enum']}"
                )
    return errors


def main():
    schema = json.loads(SCHEMA_PATH.read_text())
    data = json.loads(EXAMPLE_PATH.read_text())
    errors = validate(schema, data)

    if errors:
        print(f"FAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"PASS — {len(data)} example entries all match schema/charges.schema.json")
    sys.exit(0)


if __name__ == "__main__":
    main()
