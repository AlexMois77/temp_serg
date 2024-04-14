from functools import wraps
from hw8_class import Birthday, Record, AddressBook
import pickle

Debug = True

def input_error(func):
    if Debug:
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as err:
                return f'1Give me name and phone please! {err}'
            except IndexError as err:
                return f'Give me name please! {err}'
            except KeyError as err:
                return f'Enter the argument for the command. {err}'
            except NameError as err:
                return f'Enter the argument for the command.{err}'
            except TypeError as err:
                return f'Enter the argument for the command.{err}'
            except AttributeError as err:
                return f'Enter the argument for the command.{err}'
        return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    name = name.title()
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    name = name.title()
    record = book.find(name)
    if record and old_phone in [phone.value for phone in record.phones] and new_phone.isdigit():
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Contact not find or phone isn't digital"
    
@input_error
def show_all(contacts):
    return contacts

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    name = name.title()        
    record  = book.find(name)
    if record:
        return ", ".join(str(phone) for phone in record.phones)
    else:
        return (f"Contact: {name} no found")

@input_error    
def add_birthday (args, book: AddressBook):
    name, birthday = args
    name = name.title()
    record = book.find(name)
    message = "Birthday added."
    if record:
        record.birthday = Birthday(birthday)
        return message
    else:
        None

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    name = name.title()
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    else:
        return f"No birthday found for {name}"
    
@input_error    
def birthdays(book: AddressBook):
    return str(book.get_upcoming_birthdays(book))

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
 
def main():
    # book = AddressBook()
    print("Welcome to the assistant bot!")
    book = load_data()
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Enter a command, please, \nfrom: hello, add, change, all, phone, \nadd-birthday, show-birthday, birthdays, \nexit or close")
    save_data(book)        

if __name__ == "__main__":
    main()
