import os
import subprocess


def add_certs():
    # Получаем путь к директории с сертификатами
    cert_dir = os.path.join(os.path.dirname(__file__), 'certs')

    # Пути к сертификатам
    crl_file = os.path.join(cert_dir, 'guc2022.crl')
    crt_file = os.path.join(cert_dir, 'ucfk_2024.crt')
    command_crl = ['certutil.exe', '-addstore', '-enterprise', 'ca', crl_file]
    command_crt = ['certutil.exe', '-addstore', '-enterprise', 'ca', crt_file]

    try:
        result_crl = subprocess.run(command_crl, capture_output=True, text=True, check=True)
        print(f"Результат добавления CRL: {result_crl.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении CRL: {e.stderr}")

    try:
        result_crt = subprocess.run(command_crt, capture_output=True, text=True, check=True)
        print(f"Результат добавления CRT: {result_crt.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении CRT: {e.stderr}")


def remove_certs():
    command_del_crl = ['certutil.exe', '-delstore', 'ca', 'guc2022.crl']
    command_del_crt = ['certutil.exe', '-delstore', 'ca', 'ucfk_2024.crt']
    try:
        result_del_crl = subprocess.run(command_del_crl, capture_output=True, text=True, check=True)
        print("Результат удаления CRL:", result_del_crl.stdout)
    except subprocess.CalledProcessError as e:
        print("Ошибка при удалении CRL:", e.stderr)

    try:
        result_del_crt = subprocess.run(command_del_crt, capture_output=True, text=True, check=True)
        print("Результат удаления CRT:", result_del_crt.stdout)
    except subprocess.CalledProcessError as e:
        print("Ошибка при удалении CRT:", e.stderr)
