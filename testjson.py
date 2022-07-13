import json

FILE_NAME = "htmlparsing.json"
with open(FILE_NAME) as f:
    numbers = json.load(f)
print(numbers)