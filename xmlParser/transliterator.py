class Transliterator:
    def __init__(self):
        self.cyrillic_to_latin = {
            'А': 'A', 'а': 'a', 
            'АЕ': 'AYE', 'ае': 'aye', 'Ае': 'Aye',
            'Б': 'B', 'б': 'b', 
            'В': 'V', 'в': 'v', 
            'Г': 'G', 'г': 'g', 
            'ГА': 'GHA', 'га': 'gha', 'Га': 'Gha', 
            'Д': 'D', 'д': 'd', 
            'ДЖА': 'JA', 'джa': 'ja',
            'ДЖУ': 'JU', 'джу': 'ju',
            'ДЖ': 'DJ', 'дж': 'dj', 'Дж': 'Dj',
            'Е': 'E', 'е': 'e', 
            'Ё': 'Yo', 'Ё': 'YO', 'ё': 'yo', 
            'Ж': 'Zh', 'Ж': 'ZH', 'ж': 'zh', 
            'З': 'Z', 'з': 'z', 
            'И': 'I', 'и': 'i', 
            'ИЕ': 'IYE', 'ие': 'iye', 'Ие': 'Iye',
            'Й': 'Y', 'й': 'y', 
            'К': 'K', 'к': 'k', 
            'КИ': 'QI', 'ки': 'qi', 
            'КУ': 'QU', 'ку': 'qu', 'Ку': 'Qu', 
            'Л': 'L', 'л': 'l', 
            'М': 'M', 'м': 'm', 
            'Н': 'N', 'н': 'n', 
            'О': 'O', 'о': 'o', 
            'П': 'P', 'п': 'p', 
            'Р': 'R', 'р': 'r', 
            'С': 'S', 'с': 's', 
            'Т': 'T', 'т': 't', 
            'У': 'U', 'у': 'u', 
            'Ф': 'F', 'ф': 'f', 
            'Х': 'Kh', 'Х': 'KH', 'х': 'kh', 
            'Ц': 'Ts', 'Ц': 'TS', 'ц': 'ts', 
            'Ч': 'Ch', 'Ч': 'CH', 'ч': 'ch', 
            'Ш': 'Sh', 'Ш': 'SH', 'ш': 'sh', 
            'Щ': 'Sch', 'Щ': 'SCH', 'щ': 'sch', 
            'Ъ': '', 'ъ': '', 
            'Ы': 'Y', 'ы': 'y', 
            'ЫЕ': 'YYE', 'ые': 'yye', 'Ые': 'Yye',
            'Ь': '', 'ь': '', 
            'Ю': 'Iu', 'Ю': 'IU', 'ю': 'iu', 
            'ЮК': 'YUK', 'юк': 'yuk',
            'Я': 'Ya', 'Я': 'YA', 'я': 'ya'
        }

        self.mixed_dict = {'Н': 'H', 'С': 'C', 'Т': 'T', 'В': 'B', 'Р': 'P', 'О': 'O', 'К': 'K', 'Х': 'X', 'А': 'A', 'Е': 'E', 'М': 'M'}

        # Латиница -> кириллица (инвертируем правила)
        self.latin_to_cyrillic = {v: k for k, v in self.cyrillic_to_latin.items()}

    def to_latin(self, text):
        """Перевод текста с кириллицы на латиницу"""
        result = []
        for char in text:
            result.append(self.cyrillic_to_latin.get(char, char))  # Если символ отсутствует в правилах, оставляем его
        return ''.join(result)

    def to_cyrillic(self, text):
        """Перевод текста с латиницы на кириллицу"""
        i = 0
        result = []
        while i < len(text):
            # Проверяем возможные трехсимвольные комбинации
            if i + 2 < len(text) and text[i:i+3] in self.latin_to_cyrillic:
                result.append(self.latin_to_cyrillic[text[i:i+3]])
                i += 3
            # Проверяем возможные двухсимвольные комбинации
            elif i + 1 < len(text) and text[i:i+2] in self.latin_to_cyrillic:
                result.append(self.latin_to_cyrillic[text[i:i+2]])
                i += 2
            else:
                result.append(self.latin_to_cyrillic.get(text[i], text[i]))  # Обрабатываем однобуквенные символы
                i += 1
        return ''.join(result)

    def preprocess_mixed_cyrillic_latin(self, text):
        corrected_text = ''.join([self.mixed_dict.get(char, char) for char in text])
        return corrected_text