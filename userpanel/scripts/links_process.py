import os
import re


def process_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    updated_content = re.sub(r'<a[^>]*>', '', content)
    updated_content = updated_content.replace('</a>', '')

    for keyword, replacement_link in replacements.items():
        updated_content = updated_content.replace(keyword,
                                                  f'<a href="{replacement_link}">{keyword}</a>')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def main_script(directory, replacements):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, replacements)


