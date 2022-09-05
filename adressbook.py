import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re

import commands


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
        with open('contacts.txt', "wb") as file:
            pickle.dump(self.data, file)

    @staticmethod
    def read_from_file():
        with open('contacts.txt', "rb") as file:
            try:
                content = pickle.load(file)
            except EOFError:
                return None
            return content

    def __find_phone(self, symbols_for_search):
        """
        Looks up contacts by phone
        :param symbols_for_search:
        :return: result
        """
        result = {}
        for name, record in self.data.items():
            phones = record.phones
            found_phones = list(
                filter(lambda phone_for_data:
                       phone_for_data.value if symbols_for_search in phone_for_data.value else False, phones))

            if found_phones:
                result[name] = record
                continue
        return result

    def __find_name(self, symbols_for_search):
        """
        Looks up contacts by name
        :param symbols_for_search:
        :return: result
        """
        result = {}
        for name in self.data:
            if symbols_for_search in name:
                result[name] = self.data[name]
        return result

    def find_contacts(self, symbols_for_search):
        """
        Calls the method find_phone or find_name
        :param symbols_for_search:
        :return: result or string
        """
        if symbols_for_search[0] == "+" or symbols_for_search.isdigit():
            result = self.__find_phone(symbols_for_search)
        else:
            result = self.__find_name(symbols_for_search)
        return result if result else 'No contact with such symbols'


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, phone_to_setter):
        """
        setter for phone
        :param phone_to_setter:
        """
        if re.match(r'^\+1?\d{9,20}$', phone_to_setter):
            self._value = phone_to_setter
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
        instance_phone = Phone()
        instance_phone.value = new_phone
        self.phones.append(instance_phone)

    def change_phone(self, old_phone, new_phone):
        """
        Changes an existing number
        :param old_phone:
        :param new_phone:
        """
        current_phone = self.get_phone(old_phone)
        if current_phone:
            instance_phone = Phone()
            instance_phone.value = new_phone
            phone_examination = self.phones.append(instance_phone)
            if phone_examination == instance_phone:
                self.phones.remove(current_phone)
        else:
            print('The phone number not exist')

    def delete_phone(self, phone_to_delete):
        """
        Deletes a number
        :param phone_to_delete:
        """
        current_phone = self.get_phone(phone_to_delete)
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
        for phone_from_data in self.phones:
            if phone_from_data.value == new_phone:
                return phone_from_data
        return False


def get_name_and_phone():
    """
    To avoid duplication
    """
    name = input('Enter name:\n')
    input_phone = input('Enter phone number: \n')
    return name, input_phone


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
        commands.simple(command)
        commands.show(command, adressbook)
        commands.phone_command(command, adressbook)

        if command == 'birthday':
            name = input('Enter name:\n')
            if adressbook.is_data(name):
                record_change = adressbook.data[name]
                print('Days to birthday:', record_change.days_to_birthday())
        elif command == 'find':
            symbols_for_search = input('Enter the characters you want to search for:\n')
            print(adressbook.find_contacts(symbols_for_search))


if __name__ == '__main__':
    main()
