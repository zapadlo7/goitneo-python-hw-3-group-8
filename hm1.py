def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) == "Invalid number of arguments. Usage: phone [name]":
                return "Give me name please."
            else:
                return "Give me name and phone please."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments. Usage: change [name] [phone]")
    
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"Phone number updated for contact '{name}'."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments. Usage: phone [name]")
    
    name = args[0]
    if name in contacts:
        return f"Phone number for contact '{name}' is {contacts[name]}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    else:
        return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args

    contacts = {}
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
                print(add_contact(args, contacts))
            except ValueError as e:
                print(e)
        elif command == "change":
            try:
                print(change_contact(args, contacts))
            except ValueError as e:
                print("Error:", e)
        elif command == "phone":
            try:
                print(show_phone(args, contacts))
            except ValueError as e:
                print("Error:", e)
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
