import os
import re


def process_dots_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # حذف یکی از دو نقطه کنار هم
    content = re.sub(r'\.{2,}', '.', content)

    # تغییر خطوط پس از نقاط
    modified_content = re.sub(r'\.(?!$)', '.\n', content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)


def process_directory_dots_text(directory_path):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                process_dots_text(file_path)
