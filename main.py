from collections import UserDict
from datetime import datetime
from re import findall


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        if (not phone.isdigit()) or len(phone) != 10:
            raise ValueError
        Field.value.fset(self, phone)


class Birthday(Field):
    def __str__(self):
        @Field.value.setter
        def value(self, birthday):
            birthday = findall(r"\b(?:0?[1-9]|[12]\d|3[01])[-/. ](?:0?[1-9]|1[0-2])[-/. ](?:19\d\d|20\d\d)\b|\b(?:19\d\d|20\d\d)[-/. ](?:0?[1-9]|1[0-2])[-/. ](?:0?[1-9]|[12]\d|3[01])\b", birthday)
            if len(birthday) != 0:
                Field.value.fset(self, birthday[0])
            else:
                Field.value.fset(self, None)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if phone == p.value:
                self.phones.remove(p)

    def edit_phone(self, phone_1, phone_2):
        for i in self.phones:
            if i.value == phone_1:
                i.value = phone_2
                return
        raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if phone == p.value:
                return p

    def days_to_birthday(self):

        if self.birthday.value.__class__ is str:
            today = datetime.today().date()

            char = findall(r'[-/. ]', self.birthday.value)[0]

            list_data = self.birthday.value.split(char)

            if len(list_data[-1]) > 2:
                list_data.reverse()

            if int(list_data[0]) <= today.year:

                if int(list_data[1]) <= today.month:

                    list_data[0] = str(today.year + 1) if int(list_data[2]) < today.day else today.year

            str_date = f'{list_data[0]}{list_data[1]}{list_data[2]}'

            date_birthday = datetime.strptime(str_date, '%Y%m%d').date()

            return (str((date_birthday - today).days) + ' days')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    list_data = []

    def add_record(self, value):
        self.data.update({value.name.value: value})

    def find(self, value):
        if value in self.data:
            return self.data[value]

    def delete(self, value):
        if value in self.data:
            del self.data[value]

    def iterator(self, iteration=1, records=5):
        for i in range(iteration):
            self.paige = ""

            if len(self.list_data) == 0:
                self.list_data = self.data.copy()

            while not (len(self.paige.split('.')) == records or len(self.list_data) == 0):
                key = next(iter(self.list_data))
                self.paige += str(self.data[key]) + '.\n'
                self.list_data.pop(key)

            yield self.paige
