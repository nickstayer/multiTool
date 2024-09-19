from datetime import datetime
import os
 
class Logger:
    def __init__(self, log_dir):
        # Формируем имя файла с текущей датой
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.log_file = f"{log_dir}/log_{current_date}.txt"
 
    def log(self, message, print_in_console = True):
        try:
            with open(self.log_file, 'a', encoding='windows-1251') as file:
                line = f"{datetime.now()}: {message}\n"
                file.write(line)
                if print_in_console:
                    print(line[:-1].replace("\t", " "))
        except Exception as e:
            print(f"Ошибка при записи лога: {e}")

    def chapter(self):
        if(os.path.exists(self.log_file)):
            try:
                with open(self.log_file, 'a', encoding='windows-1251') as file:
                    file.write(f"\n\n\n")
            except Exception as e:
                print(f"Ошибка при записи лога: {e}")

    def paragraph(self):
        if(os.path.exists(self.log_file)):
            try:
                with open(self.log_file, 'a', encoding='windows-1251') as file:
                    file.write(f"\n")
            except Exception as e:
                print(f"Ошибка при записи лога: {e}")