from utils import date_to_components


class Guest:
    def __init__(self, firstName="", middleName="", lastName="", birthDate="", supplierInfo=""):
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.birthDate = birthDate
        self.supplierInfo = supplierInfo

    def __eq__(self, other):
        if isinstance(other, Guest):
            return (self.firstName == other.firstName and
                    self.lastName == other.lastName and
                    self.birthDate == other.birthDate)
        return False
    

    def dict_to_guest(dictionary):
        if not 'case.declarant.person.lastName' in dictionary.keys():
            return None
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


    def get_row(self):
        date = date_to_components(self.birthDate)
        if date:
            return f"{self.lastName};{self.firstName};{self.middleName};{date[2]};{date[1]};{date[0]};{self.supplierInfo}\n"
        return None
    
