import os
import zipfile
import re
from xps import Xps


class XpsParser:
    def __init__(self, file):
        self.file = file

    def parse(self):
        try:
            with zipfile.ZipFile(self.file, 'r') as archive:
                file_list = archive.namelist()

                for file_name in file_list:
                    if os.path.basename(file_name) == '1.fpage':
                        with archive.open(file_name) as file:
                            dirty_lines = file.read().decode('utf-8').splitlines()
                            clean_lines = self.clean_lines(dirty_lines)
                            xps = self.create_xps_instance(clean_lines)
                            return xps
        except Exception as e:
            print(f"Произошла ошибка при парсинге XPS файла: {e}")

    @staticmethod
    def extract_unicode_string(line):
        match = re.search(r'UnicodeString="([^"]+)"', line)
        if match:
            return match.group(1)
        return None

    def clean_lines(self, dirty_lines):
        my_list = []
        for line in dirty_lines:
            clean_line = self.extract_unicode_string(line)
            if not self.is_null_or_empty(clean_line):
                my_list.append(clean_line)
        return my_list

    @staticmethod
    def is_null_or_empty(s):
        return s is None or s == ''

    @staticmethod
    def create_xps_instance(lines):
        return Xps(lines[0], lines[1], lines[2], lines[3])
