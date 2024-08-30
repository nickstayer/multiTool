import requests
from bs4 import BeautifulSoup
import os

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "accept-encoding": "gzip, deflate",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }


def download_text_file(*, url: str, save_path: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text.replace("\r\n", "\r"))
        print(f"Файл успешно загружен и сохранен в: {save_path}")
        return save_path
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Другая ошибка: {err}")


def get_links(url: str):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    file_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        file_links.append(href)
    return file_links
