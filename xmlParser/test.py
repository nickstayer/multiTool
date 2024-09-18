import pytest
import sys
import os
from guest import Guest
from xmlParser import date_to_components
from xmlParser import get_row
from xmlParser import get_new_file_name
from xmlParser import get_path
from xmlParser import write_to_csv
from xmlParser import out_dir
from xmlParser import out_file
from xmlParser import clear_directory


def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


out_dir_test = os.path.join(get_current_dir(), "testdata", "out")
out_file_test = os.path.join(out_dir_test, "guests.csv")


@pytest.mark.parametrize("date, expected", [
    ("10.09.2024", ["10", "9", "2024"]),
    ("10/09/2024", []),
])
def test_date_to_components(date, expected):
    result = date_to_components(date)
    assert result == expected


@pytest.mark.parametrize("lastName, firstName, middleName, birthDate, supplierInfo, expected", [
    ("Махновец", "Кирилл", "Афонасьевич", "18.09.1991", "7400000008005302", "Махновец;Кирилл;Афонасьевич;1991;9;18;7400000008005302\n"),
    ("Махновец", "Кирилл", "", "18.09.1991", "7400000008005302", "Махновец;Кирилл;;1991;9;18;7400000008005302\n"),
])
def test_get_row(lastName, firstName, middleName, birthDate, supplierInfo, expected):
    guest = Guest()
    guest.firstName = firstName
    guest.lastName = lastName
    guest.middleName = middleName
    guest.birthDate = birthDate
    guest.supplierInfo = supplierInfo
    result = get_row(guest)
    assert result == expected


@pytest.mark.parametrize("counter, expected", [
    (0, os.path.join(out_dir, "guests.csv")),
    (999, os.path.join(out_dir, "guests.csv")),
    (1000, os.path.join(out_dir, "guests_1.csv")),
    (2000, os.path.join(out_dir, "guests_2.csv")),
])
def test_get_new_file_name(counter, expected):
    result = get_new_file_name(counter, out_file)
    assert result == expected


@pytest.mark.parametrize("input, expected", [
    (rf"""{out_dir}""", out_dir),
    ("", None),
])
def test_get_path(input, expected):
    result = get_path(input)
    assert result == expected


def test_guest_comparer():
    guest1 = Guest("Рафиков", "Римович", "Марс", "27.01.1964", "7400000008002661")
    guest2 = Guest("Люблин", "СЕРГЕЕВИЧ", "Никита", "27.01.1992", "7400000008005302")
    guest3 = Guest("Люблин", "", "Никита", "27.01.1992", "")
    guests = [guest1, guest2]
    result = guest3 in guests
    assert result == True


def test_write_to_csv():
    guest1 = Guest("Рафиков", "Римович", "Марс", "27.01.1964", "7400000008002661")
    guest2 = Guest("Люблин", "СЕРГЕЕВИЧ", "Никита", "27.01.1992", "7400000008005302")
    guests = [guest1, guest2]
    clear_directory(out_dir_test)
    csv_file = write_to_csv(guests, out_file_test)
    with open(csv_file, "r") as file:
        result = len(file.readlines())
    assert result == 2
