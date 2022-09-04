import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re

from simple_commands import simple
from show_commands import show
from phone_commands import phone_command


# from save import save_adressbook


class Field:
    def __init__(self):
        self._value = ''

    @property
    def value(self):
        """
        getter for phone and birthday
        :return: self._value
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class AddressBook(UserDict, Field):
    def is_data(self, name) -> bool:
        return name in self.data

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        for key, record in self.data.items():
            yield key, record

    def save_to_file(self):
        with open('saved.txt', "wb") as file:
            pickle.dump(self.data, file)

    @staticmethod
    def read_from_file():
        with open('saved.txt', "rb") as file:
            try:
                content = pickle.load(file)
            except EOFError:
                return None
            return content


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        """
        setter for phone
        :param phone:
        """
        if re.match(r'^\+1?\d{9,20}$', phone):
            self._value = phone
        else:
            print('Number must be minimum 9 digits maximum 20 and start with \'+\'')


class Birthday(Field):
    @Field.value.setter
    def value(self, birthday):
        """
        setter for birthday
        :param birthday:
        :return:
        """
        if int(birthday.year) <= 2022 and int(birthday.month) <= 12 and int(birthday.day) <= 31:
            self._value = datetime(year=datetime.now().year, month=int(birthday.month),
                                   day=int(birthday.day))
        else:
            print('Birthday entered incorrectly')


class Record:
    def __init__(self, new_name, birthday=None):
        self.name = Name()
        self.name.value = new_name
        self.phones = []
        self.birthday = Birthday()
        if birthday:
            self.birthday.value = birthday

    def days_to_birthday(self):
        """
        Returns the number of days until the contact's birthday
        :return:
        """
        if not self.birthday:
            return 'You did not enter a birthday'
        now = datetime.now()
        if int(self.birthday.value.month) <= int(now.month) and int(self.birthday.value.day) != int(now.day):
            days_to_birthday = self.birthday.value - now.replace(year=(int(now.year) - 1)) + timedelta(days=1)
            return days_to_birthday.days
        days_to_birthday = self.birthday.value - now + timedelta(days=1)
        return days_to_birthday.days

    def add_contact(self, new_phone):
        """
        Adds contact to adressbook
        :param new_phone:
        """
        phone = Phone()
        phone.value = new_phone
        self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        """
        Changes an existing number
        :param old_phone:
        :param new_phone:
        """
        current_phone = self.get_phone(old_phone)
        if current_phone:
            phone = Phone()
            phone.value = new_phone
            phone_examination = self.phones.append(phone)
            if phone_examination == phone:
                self.phones.remove(current_phone)
        else:
            print('The phone number not exist')

    def delete_phone(self, phone):
        """
        Deletes a number
        :param phone:
        """
        current_phone = self.get_phone(phone)
        if current_phone:
            self.phones.remove(current_phone)
        else:
            print('The phone number not exist')

    def get_phone(self, new_phone):
        """
        Checks if a number exists,
        :param new_phone:
        :return: phone or False
        """
        for phone in self.phones:
            if phone.value == new_phone:
                return phone
        return False


def get_name_and_phone():
    """
    To avoid duplication
    """
    name = input('Enter name:\n')
    phone = input('Enter phone number: \n')
    return name, phone


def find_contacts(name_of_phone, adressbook):
    """
    Looks up contacts by name or number
    :param name_of_phone:
    :param adressbook:
    :return: result or string
    """
    result = {}
    if name_of_phone == '1':
        name_to_find = input('Enter name:\n')

        for name in adressbook:
            if name_to_find in name:
                result[name] = adressbook[name]

    elif name_of_phone == '2':
        phone_to_find = input('Enter phone:\n')

        for name, record in adressbook.items():
            phones = record.phones
            s = list(filter(lambda phone: phone.value if phone_to_find in phone.value else False, phones))
            if s:
                result[name] = record
                continue
    else:
        return 'Please enter a valid choice'
    return result


def main():
    adressbook = AddressBook()
    saved = adressbook.read_from_file()
    if saved:
        for key, value in saved.items():
            adressbook.data[key] = value

    while True:
        command = input('Enter command:\n').lower()
        if command == '.':
            break
        simple(command)
        show(command, adressbook)
        phone_command(command, adressbook, get_name_and_phone, Record)

        if command == 'birthday':
            name = input('Enter name:\n')
            if adressbook.is_data(name):
                record_change = adressbook.data[name]
                print('Days to birthday:', record_change.days_to_birthday())
        elif command == 'find':
            name_or_phone = input('What parameter would you like to search for?(1 - Name, 2 - Phone)\n')
            print(find_contacts(name_or_phone, adressbook))


if __name__ == '__main__':
    main()
