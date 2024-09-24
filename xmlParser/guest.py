from utils import date_to_components
from utils import convert_date
from logger import NullLogger
from xml_parser import parse_xml
from csv_helper import CsvHelper


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
            return f"{self.lastName};{self.firstName};{self.middleName};{date[2]};{date[1]};{date[0]};{self.supplierInfo};{self.sourceFile}\n"
        return None
    

    def __str__(self):
        return f"{self.lastName} {self.firstName} {self.middleName} {self.birthDate}, {self.supplierInfo}".replace("  ", " ")
    
    def get_guests_from_xml_files(files, logger = None):
        logger = logger or NullLogger()
        guest_list = []
        file_counter = 0
        dub_counter = 0
        fail_counter = 0
        for file in files:
            file_counter += 1
            print(f"{file}")
            dictionary = parse_xml(file)
            guest = Guest.dict_to_guest(dictionary)
            if guest:
                guest.sourceFile = file
                if not guest in guest_list:
                    guest_list.append(guest)
                else:
                    in_list_guests = [g for g in guest_list if g == guest]
                    logger.log(f"Внимание. Попытка добавить гостя:\t{guest}.\tФайл-источник:\t{guest.sourceFile}")
                    for g in in_list_guests:
                        dub_counter += 1
                        logger.log(f"В списке уже есть гость с данными:\t{g}.\tФайл-источник:\t{g.sourceFile}")
            else:
                fail_counter += 1
                logger.log(f"Внимание. Не удалось получить информацию о госте:\t{file}")
        logger.paragraph()
        logger.log(f"Обработано xml:\t{file_counter}")
        logger.log(f"Попыток добавить дубли:\t{dub_counter}")
        logger.log(f"Не удалось получить информацию:\t{fail_counter}")
        return guest_list
    
    def get_guests_from_csv_files(files, logger = None):
        logger = logger or NullLogger()
        guest_list = []
        file_counter = 0
        fail_counter = 0
        for file in files:
            file_counter += 1
            print(f"{file}")
            dict_list = CsvHelper(file).read_csv()
            guests = Guest.dict_list_to_guests(dict_list)
            if guests:
                guest_list.extend(guests)
            else:
                fail_counter += 1
                logger.log(f"Внимание. Не удалось получить информацию о гостях:\t{file}")
        guest_set = set(guest_list)
        logger.paragraph()
        logger.log(f"Обработано csv:\t{file_counter}")
        logger.log(f"Попыток добавить дубли:\t{len(guest_list) - len(guest_set)}")
        logger.log(f"Не удалось получить информацию:\t{fail_counter}")
        return list(guest_set)