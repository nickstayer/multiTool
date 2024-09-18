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
