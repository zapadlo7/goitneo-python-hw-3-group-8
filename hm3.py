from collections import UserDict, defaultdict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Phone must be a string")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value=None):
        if value is not None:
            try:
                datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError("Birthday must be in the format DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, *phones):
        for phone in phones:
            if phone not in [p.value for p in self.phones]:
                self.phones.append(Phone(phone))
            else:
                print(f"Phone number '{phone}' already exists for contact '{self.name.value}'. Skipping.")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Only one birthday allowed per contact")
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value.lower()
        self.data[name] = record

    def delete_record(self, name):
        del self.data[name]

    def find(self, name):
        name = name.lower()
        return self.data.get(name)

    def add_birthday(self, name, birthday):
        record = self.data.get(name.lower())
        if record:
            record.add_birthday(birthday)
        else:
            raise ValueError(f"Contact '{name}' not found.")

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays_per_week = defaultdict(list)

        for record in self.data.values():
            name = record.name.value
            birthday = record.birthday.value
            birthday = datetime.strptime(birthday, '%d.%m.%Y').date()

            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if birthday_this_year.weekday() in [5, 6]:
                birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                birthday_weekday = birthday_this_year.strftime("%A")
                birthdays_per_week[birthday_weekday].append(name)

        next_week = today + timedelta(days=(7 - today.weekday()))
        print("Users to congratulate next week:")
        for day in range(7):
            next_day = next_week + timedelta(days=day)
            day_of_week = next_day.strftime("%A")
            if birthdays_per_week[day_of_week]:
                print(f"{day_of_week}: {', '.join(birthdays_per_week[day_of_week])}")

    def delete(self, name):
        name = name.lower()
        for record_name, record in self.data.items():
            if record_name == name:
                del self.data[record_name]
                print(f"Contact '{name}' has been deleted.")
                return
        print(f"No contact with name '{name}' found.")

    def delete_phone(self, name, phone):
        record = self.data.get(name.lower())
        if record:
            record.remove_phone(phone)
            print(f"Phone number '{phone}' deleted for contact '{name}'.")
        else:
            print(f"Contact '{name}' not found.")

    def find_phone(self, phone):
        found_contacts = []
        for record in self.data.values():
            if any(phone == phone_number.value for phone_number in record.phones):
                found_contacts.append(record)
        return found_contacts

def main():
    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args

    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            try:
                if len(args) != 2:
                    raise ValueError("Please provide both name and phone number separated by a space.")
                
                name, phone = args
                record = book.find(name)
                if record:
                    record.add_phone(phone)  
                    print(f"Phone number '{phone}' added for contact '{name}'.")
                else:
                    record = Record(name)
                    record.add_phone(phone)  
                    book.add_record(record)
                    print(f"Contact '{name}' added with phone number '{phone}'.")
            except ValueError as e:
                print("Error:", e)

        elif command == "change":
            try:
                if len(args) != 3:
                    raise ValueError("Please provide the name, old phone number, and new phone number separated by spaces.")
                
                name, old_phone, new_phone = args
                record = book.find(name)
                if record:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Phone number updated for contact '{name}'.")
                else:
                    print(f"Contact '{name}' not found.")
            except ValueError as e:
                print("Error:", e)

        elif command == "phone":
            if args:
                try:
                    name = args[0]
                    record = book.find(name)
                    if record:
                        print(f"Phone number(s) for contact '{name}' : {', '.join(str(phone) for phone in record.phones)}.")
                    else:
                        print(f"Contact '{name}' not found.")
                except ValueError as e:
                    print("Error:", e)
            else:
                print("Please provide the name of the contact.")
        elif command == "find phone":
            print("Invalid command. Please use 'find' instead.")
        elif command == "find":
            if args:
                try:
                    phone = args[0]
                    if len(phone) != 10 or not phone.isdigit():
                        raise ValueError("Invalid phone number format. Please provide a 10-digit phone number.")
                        
                    found_contacts = book.find_phone(phone)
                    if found_contacts:
                        print(f"Contacts with phone number '{phone}':")
                        for contact in found_contacts:
                            print(contact)
                    else:
                        print(f"No contacts found with phone number '{phone}'.")
                except ValueError as e:
                    print("Error:", e)
            else:
                print("Please provide the phone number to search for.")
        elif command == "all":
            if book:
                print("All contacts:")
                for name, record in book.data.items():
                    print(record)
            else:
                print("No contacts found.")

        elif command == "add-birthday":
            try:
                if len(args) != 2:
                    raise ValueError("Please provide the name, with a space, and the date of birth in the format 'DD.MM.YYYY'.")
                
                name, birthday = args
                book.add_birthday(name, birthday)
                print(f"Birthday added for contact '{name}'.")
            except ValueError as e:
                print("Error:", e)

        elif command == "show-birthday":
            if args:
                try:
                    name = args[0]
                    record = book.find(name)
                    if record:
                        print(f"Birthday for contact '{name}' is {record.birthday}.")
                    else:
                        print(f"No birthday set for contact '{name}'.")
                except ValueError as e:
                    print("Error:", e)
            else:
                print("Please provide the name of the contact.")
        elif command == "birthdays":
            book.get_birthdays_per_week()
        elif command == "delete":
            if len(args) == 1:
                name = args[0]
                book.delete(name)
            elif len(args) == 2:
                name, phone = args
                book.delete_phone(name, phone)
            else:
                print("Please provide the name of the contact to delete.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()