import json

def input_error(func):
    def handler(*args):
        try:
            return func(*args)

        except TypeError:
            return f'<<< Please check your input\nadd "Name" "phone"\nchange "Name`" "phone"\nphone "Name"\nshow all\nexit'
        
        except IndexError:
            return f'<<< Please correct your input\nadd "Name" "phone"\nchange "Name`" "phone"\nphone "Name"\nshow all\nexit'
    return handler


def is_name_occupied(name):
    '''This function checking the name'''
    with open('phone_book.txt', 'r') as pb:
        lines = pb.readlines()

    for line in lines:
        dict_pb = json.loads(line.strip())
        if dict_pb["name"] == name:
            return True

    return False

@input_error
def add(*args):
    name = args[0]
    phone = args[1]
    
    if is_name_occupied(name):
        return f'<<<This name is occupied'

    with open('phone_book.txt', 'a') as pb:
        dict_pb = {"name": name, "phone": phone}
        pb.write(json.dumps(dict_pb) + "\n")
    
    return f'<<< Add success {name.capitalize()} {phone}'

@input_error
def change(*args):
    name = args[0]
    new_phone = args[1]

    found_dict_pb = False

    with open('phone_book.txt', 'r') as pb:
        lines = pb.readlines()

    for i, line in enumerate(lines):
        dict_pb = json.loads(line.strip())
        if dict_pb["name"] == name:
            dict_pb["phone"] = new_phone
            lines[i] = json.dumps(dict_pb) + "\n"
            found_dict_pb = True
            break

    if found_dict_pb:
        with open('phone_book.txt', 'w') as pb:
            pb.writelines(lines)

        return f'<<< Change success: {name.capitalize()} has a new phone {new_phone}'
    else:
        return f'<<< "{name.capitalize()}" not found in the phone book.'

@input_error
def phones(*args):
    name = args[0]
    with open('phone_book.txt', 'r') as pb:
        lines = pb.readlines()
    for line in lines:
        dict_pb = json.loads(line.strip())
        if dict_pb['name'] == name:
            return f"<<< {name.capitalize()} phone is: {dict_pb['phone']}"


def show_all():
    with open('phone_book.txt', 'r') as pb:
        lines = pb.readlines()

    contacts = []
    for line in lines:
        entry = json.loads(line.strip())
        contact_str = f"Name: {(entry['name']).capitalize()}, Phone: {entry['phone']}"
        contacts.append(contact_str)

    return '\n'.join(contacts)

def no_command(*args):
    return '\n***Unknow command***`\nCommand availible:\nadd "Name" "phone"\nchange "Name`" "phone"\nphone "Name"\nshow all\nexit'

def parser(text: str) -> tuple[callable, tuple[str, ... ] | None]:
    text = text.lower()
    if text.startswith('add'):
        return add, text.replace('add', '').strip().split()
    elif text.startswith('change'):
        return change, text.replace('change', '').strip().split()
    elif text.startswith('phone'):
        return phones, text.replace('phone', '').strip()
    elif text == 'show all':
        return show_all, None
    return no_command, None

def main():
    print("Введи 'Hello' для початку")
    while True:
        user_input = input('>>>')
        if user_input.lower() == 'hello':
            print('<<< Hi, how can I help u\nCommand availible:\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\nshow all\nexit')
        elif user_input.lower() in ('good bye', 'exit', 'close'):
            print('Good Bye')
            break
        else:
            command, data = parser(user_input)
            if data is not None:
                result = command(*data)
            else:
                result = command()
            print(result)

if __name__ == "__main__":
    main()