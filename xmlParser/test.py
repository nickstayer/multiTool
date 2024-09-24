import pytest
import sys
import os
from guest import Guest
from utils import *
from main import out_dir
from main import out_file
from csv_helper import  CsvHelper


def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

test_dir = os.path.join(get_current_dir(), "testdata")
out_dir_test = os.path.join(test_dir, "out")
csv_dir_test = os.path.join(test_dir, "csv")
out_file_test = os.path.join(out_dir_test, "guests.csv")



@pytest.mark.parametrize("date, expected", [
    ("10.09.2024", ["10", "9", "2024"]),
    ("10/09/2024", []),
])
def test_date_to_components(date, expected):
    actual = date_to_components(date)
    assert actual == expected


@pytest.mark.parametrize("lastName, firstName, middleName, birthDate, supplierInfo, file, expected", [
    ("Махновец", "Кирилл", "Афонасьевич", "18.09.1991", "7400000008005302", "file.xml", "Махновец;Кирилл;Афонасьевич;1991;9;18;7400000008005302;file.xml\n"),
    ("Махновец", "Кирилл", "", "18.09.1991", "7400000008005302", "file.xml", "Махновец;Кирилл;;1991;9;18;7400000008005302;file.xml\n"),
])
def test_get_row(lastName, firstName, middleName, birthDate, supplierInfo, file, expected):
    guest = Guest()
    guest.firstName = firstName
    guest.lastName = lastName
    guest.middleName = middleName
    guest.birthDate = birthDate
    guest.supplierInfo = supplierInfo
    guest.sourceFile = file
    actual = guest.get_row()
    assert actual == expected


@pytest.mark.parametrize("counter, current_file, expected", [
    (0, os.path.join(out_dir, "guests_1.csv"), os.path.join(out_dir, "guests_1.csv")),
    (900,  os.path.join(out_dir, "guests_1.csv"), os.path.join(out_dir, "guests_2.csv")),
    (1800,  os.path.join(out_dir, "guests_1.csv"), os.path.join(out_dir, "guests_3.csv")),
])
def test_get_new_file_name(counter, current_file, expected):
    csv_parser = CsvHelper(out_file)
    actual = csv_parser.get_new_file_name(counter, current_file)
    assert actual == expected


@pytest.mark.parametrize("input, expected", [
    (rf"""{out_dir}""", out_dir),
    ("", None),
])
def test_get_path(input, expected):
    actual = get_path(input)
    assert actual == expected


def test_guest_comparer():
    guest1 = Guest("Рафиков", "Римович", "Марс", "27.01.1964", "7400000008002661")
    guest2 = Guest("Люблин", "СЕРГЕЕВИЧ", "Никита", "27.01.1992", "7400000008005302")
    guest3 = Guest("Люблин", "", "Никита", "27.01.1992", "")
    guests = [guest1, guest2]
    actual = guest3 in guests
    assert actual == True


def test_write_to_csv():
    clear_directory_from_csv_files(out_dir_test)
    guest1 = Guest("Рафиков", "Римович", "Марс", "27.01.1964", "7400000008002661")
    guest2 = Guest("Люблин", "СЕРГЕЕВИЧ", "Никита", "27.01.1992", "7400000008005302")
    guests = [guest1, guest2]
    csv_parser = CsvHelper(out_file_test)
    csv_file = csv_parser.write_guests_to_csv(guests, out_file_test)
    with open(csv_file, "r") as file:
        actual = len(file.readlines())
    assert actual == 2


def test_csv_parser_read():
    csv_file = os.path.join(csv_dir_test, "test_csv_parser_read.csv")
    clear_directory_from_csv_files(out_dir_test)
    csv_parser = CsvHelper(csv_file)
    dict_list = csv_parser.read_csv()
    guests = Guest.dict_list_to_guests(dict_list)
    csv_parser.write_guests_to_csv(guests, out_file_test)
    with open(out_file_test, "r") as file:
        actual = len(file.readlines())
    assert actual == 4


@pytest.mark.parametrize("input, expected", [
    ("2020-12-20", "20.12.2020"),
    ("20.12.2020", "20.12.2020"),
    ("20/12/2020", None),
])
def test_convert_date(input, expected):
    actual = convert_date(input)
    assert actual == expected


def test_get_xml_csv_files():
    both_format_dir = os.path.join(test_dir, "both_format")
    xml_list, csv_list = get_xml_csv_files(both_format_dir)
    assert len(csv_list) == 2
    assert len(xml_list) == 6


def test_get_guests_from_csv_files():
    csv_path = os.path.join(test_dir, "csv")
    xml_files, csv_files = get_xml_csv_files(csv_path)
    actual = Guest.get_guests_from_csv_files(csv_files)
    assert len(actual) == 644


def test_get_guests_from_xml_files():
    xml_path = os.path.join(test_dir, "xml")
    xml_files, csv_files = get_xml_csv_files(xml_path)
    actual = Guest.get_guests_from_xml_files(xml_files)
    assert len(actual) == 2