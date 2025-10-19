import json


def java_like_switch(value):
    match value:
        case 'a':
            return "You chose A"
        case 'b':
            return "You chose B"
        case 'c':
            return "You chose C"
        case _:
            return "Invalid choice"


def read_file(filename, key):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            #print(data.get(key, 'Name not found'))
            return data.get(key, "")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")


data = read_file("./details.json", "Air1")
print(data)
if 'basic' in data:
    print(data['basic'])