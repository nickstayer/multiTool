from web import download_text_file
from web import get_links
import os

current_dir = os.path.dirname(__file__)
forms_dir = os.path.join(current_dir, "forms")

if not os.path.exists(forms_dir):
    os.makedirs(forms_dir)


def main():
    try:
        with open("url.txt", "r") as url_file:
            url = url_file.read().strip()
        base_url = get_base_url(url=url)
        file_links = get_links(url)
        with open("forms_names.txt", "r") as forms_names_file:
            need_forms_names = [form.replace("\n", "") for form in forms_names_file.readlines() if form]
        counter = 0
        for link in file_links:
            full_url = base_url + link if not link.startswith("http") else link
            if os.path.basename(full_url) in need_forms_names:
                download_text_file(url=full_url, save_path=forms_dir + "\\" + os.path.basename(full_url))
                counter += 1
        input(f"Загружено форм: {counter}")
    except Exception as e:
        print(e)


def get_base_url(*, url) -> str:
    url_components = url.split("/")
    base_url = url_components[0] + "//" + url_components[2]
    return base_url


if __name__ == "__main__":
    main()
