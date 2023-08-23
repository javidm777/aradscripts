import os
import re

# مسیر دایرکتوری حاوی فایل‌های .txt


aradbranding_pattern = r'<a\s+href="https?://aradbranding\.com[^>]*>(.*?)</a>'


def process_text_file(file_path, directory_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # حذف لینک‌ها به aradbranding.com از متن
    content_without_aradbranding_links = re.sub(aradbranding_pattern, r'\1', content)

    # ذخیره محتوای ویرایش شده در فایل جدید
    new_file_path = os.path.join(directory_path, os.path.basename(file_path))
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        new_file.write(content_without_aradbranding_links)


def run_text_process(dir):
    txt_files = [f for f in os.listdir(dir) if f.endswith(".txt")]
    # پردازش هر فایل .txt
    for txt_file in txt_files:
        txt_file_path = os.path.join(dir, txt_file)
        process_text_file(txt_file_path, dir)
        print(f"Processed: {txt_file_path}")


