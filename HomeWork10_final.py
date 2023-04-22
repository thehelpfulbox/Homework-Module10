from collections import UserDict


class Field:

    def __init__(self, value=None):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    
class Name(Field):
    pass


class Phone(Field):
    pass


class Record:

    def __init__(self, name:Name, phone:Phone=None):
        self.name = name
        self.phones = [phone] if phone else []

    def __str__(self):
        return f'{self.name.value}: {self.phones}'
        
    
    def __repr__(self):
        return str(self.phones)
    
    def add_number(self, phone:Phone):
        self.phones.append(phone)
    
    def del_phone(self, phone):
        for p in self.phones:
            if p == phone:
                self.phones.remove(p)
                return f"Phone number {phone} was deleted from contact {self.name}"
        return f'{phone} was not found in list'
    
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for p in self.phones:
            if p.value == old_phone.value:
                self.phones[self.phones.index(p)] = new_phone
                return f"Phone number {old_phone} has been substituted with {new_phone} for contact {self.name}"
        return f'{old_phone} not in list'
 
    
class Addressbook(UserDict):
    def add_record(self, record: Record):
        if self.get(record.name.value):
            return f'{record.name.value} is already in contacts'
        self.data[record.name.value] = record
        return f'{record.name.value} with {record.phones} phone was successfully added in contacts'

    def show_all(self):
        return self.data

    def phone(self, name):
        try:
            return self.data[name]
        except KeyError:
            return f'Contact {name} is absent'

    def delete_record(self, name):
        del self.data[name.value]


contacts = Addressbook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, TypeError, ValueError):
            return "Command was entered incorrectly."
        except KeyError:
            return "Can't find such name in the database."
    return inner


@input_error
def add_new_contact(*data):
    name = Name(data[0].lower().capitalize())
    raw_phone = "".join(data[1:])
    sanitized_phone = ""
    for i in raw_phone:
        if not i.isdigit():
            continue
        else:
            sanitized_phone += i
    if len(sanitized_phone) == 0:
        return f"Can't create the record '{name}'. The number that you entered does not contain any digits."
    else:
        phone = Phone(sanitized_phone)
    record = contacts.get(name.value)
    if record:
        record.add_number(phone)
        return f'Phone number {phone} was added successfully to contact {name}'
    record = Record(name, phone)
    contacts.add_record(record)
    return f'Contact {name} with phone number {phone} was added successfully'


@input_error
def change_phone(*data):
    name = Name(data[0].lower().capitalize())
    old_phone = Phone(data[1])
    new_phone = Phone(data[2])
    rec = contacts.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact with name {name}"


@input_error
def show_phone(*result):
    name = Name(result[0].lower().capitalize())
    if name.value in contacts.data:
        for key, val in contacts.data.items():
            record = contacts.data[key]
            if name.value == key:
                return f"{name.value}: {', '.join(str(phone) for phone in record.phones)}"
    

@input_error
def show_all_contacts(*result):
    if contacts:
        return '\n'.join([f'{phones}' for name, phones in contacts.data.items()])
    return "You have no contacts yet"    
    

@input_error
def hello(*result):
    return """How can I help you?
        - To add contact, type: <add name number>
        - To show contact details of the person, type: <phone name>
        - To show all contacts in the directory, type: <show all> 
        - To change contact in the directory, type: <change name old_number new_number>
        - To exit the program, type: <exit> or <close> or <good bye>"""


@input_error
def end(*result):
    return "Good bye!"


def unknown_input(*command):
    return "Unknown command"


COMMANDS = {'hello': hello,
            'add': add_new_contact,
            'good bye': end,
            'exit': end,
            'close': end,
            'show all': show_all_contacts,
            'change': change_phone,
            'phone': show_phone,
            }


def parser(user_input:str):
    user_input = user_input.lower()
    # for kword, command in COMMANDS.items():
    #     if user_input.startswith(kword):
    #         return command, user_input.replace(kword, '').strip().split()
    # return unknown_input, user_input

    if user_input.startswith("add"):
        return add_new_contact, user_input.removeprefix("add").strip().split()
    elif user_input.startswith("hello"):
        return hello, user_input.removeprefix("hello").strip().split()
    elif user_input.startswith("change"):
        return change_phone, user_input.removeprefix("change").strip().split()
    elif user_input.startswith("phone"):
        return show_phone, user_input.removeprefix("phone").strip().split()
    elif user_input.startswith("show all"):
        return show_all_contacts, user_input.removeprefix("show all").strip().split()
    elif user_input.startswith("exit") or user_input.startswith("close") or user_input.startswith("good bye"):
        return end, user_input
    else:
        return unknown_input, user_input


def main():
    print(hello())
    while True:
        user_input = (input(">>>")) 
        command, data = parser(user_input)
        print(command(*data))
        if command == end:
            break
            

if __name__ == '__main__':
    main()
