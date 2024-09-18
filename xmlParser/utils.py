import os

def date_to_components(date: str):
    components = date.split('.')
    if len(components) < 3:
        return []
    new_components = []
    for c in components:
        if c.startswith('0'):
            new_components.append(c[1:])
        else:
            new_components.append(c)
    return new_components


def get_path(input: str):
    input = input.replace("\"", "")
    if os.path.exists(input):
        return input
    else:
        return None


def get_lower_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower()


def clear_directory_from_csv_files(directory_path):
    try:
        if os.path.isdir(directory_path):
            print(f"Очищаю: {directory_path}")
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    if get_lower_file_extension(file_path) == ".csv":
                        os.remove(file_path)
        else:
            print(f"Указанный путь '{directory_path}' не является директорией.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

