import pickle

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = birthday

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        from datetime import datetime, timedelta

        upcoming_birthdays = []
        today = datetime.now().date()
        week_later = today + timedelta(days=7)

        for record in self.records:
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday, "%d.%m.%Y").date()
                if today <= birthday_date <= week_later:
                    upcoming_birthdays.append({
                        "name": record.name,
                        "birthday": record.birthday
                    })

        return upcoming_birthdays

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def parse_input(user_input):
    return user_input.split()

def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    if phone:
        record.add_phone(phone)
    return "Contact updated." if record else "Contact added."

def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        if old_phone in record.phones:
            record.phones[record.phones.index(old_phone)] = new_phone
            return "Phone number updated."
        return "Old phone number not found."
    return "Contact not found."

def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return ", ".join(record.phones) if record.phones else "No phone numbers."
    return "Contact not found."

def list_all_contacts(book):
    result = []
    for record in book.records:
        phones = ", ".join(record.phones) if record.phones else "No phone numbers."
        result.append(f"{record.name}: {phones}")
    return "\n".join(result) if result else "No contacts found."

def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.birthday if record.birthday else "No birthday set."
    return "Contact not found."

def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(f"{entry['name']}: {entry['birthday']}" for entry in upcoming_birthdays)
    return "No upcoming birthdays."

def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)  # Викликати перед виходом з програми
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(list_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
