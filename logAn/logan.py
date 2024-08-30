import os
from form import Form
from transfer import Transfer

HEADERS = [
    'Оператор',
    'Форма',
    'Дата Форма получена',
    'Ответ',
    'Дата Ответ получен с ftp',
    'Дата Ответ передан клиенту'
]
current_dir = os.path.dirname(__file__)
LOGS_PATH = os.path.join(current_dir, 'logs')
FILE_RESULT = os.path.join(current_dir, 'result.csv')
ENCODING = 'cp1251'
# utf-8


def main():
    input('Положите логи в папку logs/ и нажмите Enter')
    if os.path.exists(LOGS_PATH):
        write_line_in_file(line=";".join(HEADERS) + "\n", file_path=FILE_RESULT)
        log_file_paths = get_file_paths(file_extension='.log', directory_path=LOGS_PATH)
        forms, responses = get_forms_and_responses(log_file_paths=log_file_paths)
        transfers = get_transfers(forms=forms, responses=responses)
        write_transfers(transfers=transfers, file_path=FILE_RESULT)
    else:
        print(f'Нет пути {LOGS_PATH}')
    input('Кончено')


def get_transfers(*, forms, responses):
    transfers = []
    for form in forms:
        print(f'Форма {form.form_name}')
        transfer = Transfer()
        transfer.form_file_name = form.file_name
        transfer.form_name = form.form_name
        transfer.operator = form.operator
        transfer.form_received_date_time = form.date_time
        for response in responses:
            if form.form_name == response.form_name:
                transfer.response_file_name = response.file_name
                if response.operator.startswith('ftp'):
                    transfer.response_received_from_ftp_date_time = response.date_time
                if response.operator.startswith('flash'):
                    transfer.response_sent_to_client_date_time = response.date_time
                    break
        transfers.append(transfer)
    return transfers


def get_forms_and_responses(*, log_file_paths):
    total_forms = []
    total_responses = []
    for log_file_path in log_file_paths:
        print(f'Файл {log_file_path}')
        log_file_forms, log_file_responses = parse_log(log_file_path=log_file_path)
        total_forms.extend(log_file_forms)
        total_responses.extend(log_file_responses)
    return total_forms, total_responses


def get_file_paths(*, file_extension: str, directory_path: str):
    files = os.listdir(directory_path)
    paths = []
    for file in files:
        if (os.path.isfile(os.path.join(directory_path, file))
                and file_extension == get_extension(file_path=os.path.join(directory_path, file))):
            paths.append(os.path.join(directory_path, file))
    return paths


def parse_log(*, log_file_path: str):
    forms = []
    responses = []
    with open(log_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if '.xml' in line.lower():
                file_name = get_file_name_from_log_line(log_line=line)
                form = Form()
                form.file_name = file_name
                form.form_name = get_form_name(file_name=form.file_name)
                form.operator = get_operator_from_log_line(log_line=line)
                form.is_response = is_response(file_name=file_name)
                form.date_time = get_date_time_from_log_line(log_line=line)
                if is_response(file_name=file_name):
                    responses.append(form)
                else:
                    forms.append(form)
    return forms, responses


def get_operator_from_log_line(*, log_line: str) -> str:
    arr = log_line.split(' ')
    if len(arr) > 2:
        source = switch_source(source_value=arr[2])
        return source


def get_date_time_from_log_line(*, log_line: str) -> str:
    arr = log_line.split(' ')
    if len(arr) > 1:
        result = f'{arr[0]} {arr[1]}'
        return result


def switch_source(*, source_value: str) -> str:
    match source_value:
        case "skb":
            return source_value
        case "rock":
            return source_value
        case "tenzor":
            return source_value
        case "flash":
            return source_value
        case "test":
            return source_value
        case _:
            return "ftp"


# file name example: Form5_12882_27340_dac040bc-e827-4037-961a-49d515d7191a
def get_file_name_from_log_line(*, log_line: str) -> str:
    strings = log_line.split(' ')
    for s in strings:
        if '.xml' in s.lower():
            return s.replace('\n', '')


# form name example: dac040bc-e827-4037-961a-49d515d7191a
def get_form_name(*, file_name: str) -> str:
    arr = file_name.lower().split('_')
    longest_part = max(arr, key=len)
    return longest_part.replace('.xml', '')


def is_response(*, file_name: str) -> bool:
    return 'response' in file_name.lower()


def get_extension(*, file_path) -> str:
    _, extension = os.path.splitext(file_path)
    return extension


def write_transfers(*, transfers, file_path: str):
    for transfer in transfers:
        write_line_in_file(line=f'{transfer.operator};'
                           f'{transfer.form_file_name};'
                           f'{transfer.form_received_date_time};'
                           f'{transfer.response_file_name};'
                           f'{transfer.response_received_from_ftp_date_time};'
                           f'{transfer.response_sent_to_client_date_time}\n', file_path=file_path
                           )


def write_line_in_file(*, line: str, file_path: str):
    mode = 'a'
    if line.startswith('Оператор'):
        mode = 'w'
    with open(file_path, mode, encoding=ENCODING) as file:
        file.write(line)


if __name__ == "__main__":
    main()
