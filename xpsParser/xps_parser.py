from parser import XpsParser
from word import Word
import os
from pathlib import Path


def main():
    current_dir = os.path.dirname(__file__)
    in_dir = os.path.join(current_dir, "in")
    out_dir = os.path.join(current_dir, "out")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    template = os.path.join(current_dir, "template.docx")
    input(f"Поместите xps файлы в папку {in_dir} и нажмите Enter")
    if os.path.exists(in_dir):
        files = list(Path(in_dir).glob("*"))
        word = Word()
        counter = 0
        for file in files:
            if file.suffix == ".xps":
                counter += 1
                parser = XpsParser(file)
                xps = parser.parse()
                if os.path.exists(template):
                    word.open(template)
                    word.insert_text_after_line("Подразделение:", xps.name.replace("1528 ", ""))
                    word.insert_text_in_table(1, 1, 2, xps.name)
                    word.insert_text_in_table(1, 2, 2, xps.passw_phrase)
                    word.insert_text_in_table(1, 3, 2, xps.passw)
                    new_file = os.path.join(out_dir, xps.name)
                    word.save_as(new_file)
                    word.close()
                else:
                    print(f"Файл {template} отсутствует")
        word.quit()
        input(f"Работа программы завершена! Обработано файлов: {counter}")
    else:
        print(f"Папка {in_dir} не существует")


if __name__ == "__main__":
    main()
