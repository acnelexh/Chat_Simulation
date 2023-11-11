import json

# JSON string
json_string = '{"name": "John", "age": 30, "city": "New York"}'

# Parse JSON string
parsed_json = json.loads(json_string)

print(parsed_json["name"])