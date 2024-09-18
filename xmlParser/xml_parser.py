import xml.etree.ElementTree as ET

def parse_element(element, parent_name=''):
    """Рекурсивно обрабатывает элементы XML и добавляет их в словарь."""
    parsed_data = {}
    tag_name = element.tag.split('}')[-1]
    full_tag_name = f"{parent_name}.{tag_name}" if parent_name else tag_name
    
    if element.text and element.text.strip():
        parsed_data[full_tag_name] = element.text.strip()
    
    if element.attrib:
        parsed_data[f"{full_tag_name}_attributes"] = element.attrib

    for child in element:
        parsed_data.update(parse_element(child, full_tag_name))

    return parsed_data


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        parsed_data = parse_element(root)
        return parsed_data
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return None
