from utils import date_to_components
from utils import convert_date


def get_ru_guest(dictionary):
    guest = Guest()
    for key, value in dictionary.items():
        if key == 'case.declarant.person.lastName':
            guest.lastName = value
        if key == 'case.declarant.person.firstName':
            guest.firstName = value
        if key == 'case.declarant.person.middleName':
            guest.middleName = value
        if key == 'case.declarant.person.birthDate':
            guest.birthDate = value
        if key == 'case.supplierInfo':
            guest.supplierInfo = value
    return guest


def get_foreign_guest(dictionary):
    guest = Guest()
    for key, value in dictionary.items():
        if key == 'case.personDataDocument.person.lastName':
            guest.lastName = value
        if key == 'case.personDataDocument.person.firstName':
            guest.firstName = value
        if key == 'case.personDataDocument.person.birthDate':
            guest.birthDate = value
        if key == 'case.supplierInfo':
            guest.supplierInfo = value
    return guest

def get_guest_from_eirrmu(dictionary):
    guest = Guest()
    for key, value in dictionary.items():
        if key == 'Фамилия':
            guest.lastName = value
        if key == 'Имя':
            guest.firstName = value
        if key == 'Отчество':
            guest.middleName = value
        if key == 'Дата рождения':
            guest.birthDate = convert_date(value)
        if key == 'Код подразделения':
            guest.supplierInfo = value
    return guest


class Guest:
    def __init__(self, firstName="", middleName="", lastName="", birthDate="", supplierInfo="", sourceFile=""):
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.birthDate = birthDate
        self.supplierInfo = supplierInfo
        self.sourceFile = sourceFile

    def __eq__(self, other):
        if isinstance(other, Guest):
            return (self.firstName == other.firstName and
                    self.lastName == other.lastName and
                    self.birthDate == other.birthDate)
        return False
    
    def __hash__(self):
        return hash((self.firstName, self.lastName, self.birthDate))
    

    def dict_to_guest(dictionary):
        if 'case.declarant.person.lastName' in dictionary.keys():
            return get_ru_guest(dictionary)
        if 'case.personDataDocument.person.lastName' in dictionary.keys():
            return get_foreign_guest(dictionary)
        if 'Фамилия' in dictionary.keys():
            return get_guest_from_eirrmu(dictionary)


    def dict_list_to_guests(dictionary_list):
        guests = []
        for dictionary in dictionary_list:
            guest = Guest.dict_to_guest(dictionary)
            guests.append(guest)
        return guests


    def get_row(self):
        date = date_to_components(self.birthDate)
        if date:
            return f"{self.lastName};{self.firstName};{self.middleName};{date[2]};{date[1]};{date[0]};{self.supplierInfo}\n"
        return None
    

    def __str__(self):
        return f"{self.lastName} {self.firstName} {self.middleName} {self.birthDate}, {self.supplierInfo}".replace("  ", " ")
    