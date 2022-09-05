from datetime import datetime


def phone_command(command: str, adressbook, get_name_and_phone, record):
    if command.split()[0] == 'add':  # Add contact
        name, phone = get_name_and_phone()
        birthday = input('Enter birthday(day month, year) or skip(enter):\n')
        try:
            birthday = datetime.strptime(birthday, "%d %B, %Y").date()
        except ValueError:
            birthday = ''
        if len(phone.split()) > 1:
            print('Enter ONE phone number')
        else:
            if name and phone:
                record_add = record(name.lower(), birthday if birthday != '' else None)
                record_add.add_contact(phone)
                adressbook.add_record(record_add)
                adressbook.save_to_file()
            else:
                print('Enter correct name and phone')

    elif command.split()[0] == 'change_phone':  # Change contact number
        name, phone = get_name_and_phone()
        new_phone = input('Enter new phone\n')
        if adressbook.is_data(name):
            record_change = adressbook.data[name]
            record_change.change_phone(old_phone=phone, new_phone=new_phone)
        else:
            print('Enter correct name')

    elif command.split()[0] == 'add_phone':  # Add contact number
        name, phone = get_name_and_phone()
        if adressbook.is_data(name):
            record_add_phone = adressbook.data[name]
            record_add_phone.add_contact(phone)
        else:
            print('Enter correct name')

    elif command.split()[0] == 'delete':  # Delete contact number
        name, phone = get_name_and_phone()
        if adressbook.is_data(name):
            record_delete = adressbook.data[name]
            record_delete.delete_phone(phone)
        else:
            print('Enter correct name')
