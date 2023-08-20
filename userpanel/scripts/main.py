import os
import xmlrpc.client


def get_wordpress_posts(wp_url, wp_username, wp_password, start_post,
                        batch_size, output_directory):
    server = xmlrpc.client.ServerProxy( wp_url + '/xmlrpc.php')

    user = wp_username
    password = wp_password
    auth = {'username': user, 'password': password}

    # تعداد تلاش‌های اتصال
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # دریافت لیست پست‌ها برای بازه داده شده
            posts = server.wp.getPosts('', user, password,
                                       {'number': batch_size,
                                        'offset': start_post - 1})

            if not posts:
                return False

            for post in posts:
                post_id = post['post_id']
                post_title = post['post_title']
                post_content = post['post_content']

                # ایجاد دایرکتوری اگر وجود نداشته باشد
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                # ایجاد فایل txt با اطلاعات پست در دایرکتوری مشخص
                file_path = os.path.join(output_directory, f'{post_id}.txt')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(post_title + '\n')
                    f.write(post_content)

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            retries += 1

    return False


if __name__ == "__main__":
    website = 'sanatmorgh.ir'
    wordpress_url = website
    wordpress_username = "talia"
    wordpress_password = "1331@1331!"

    batch_size = 100  # تعداد پست‌ها در هر گروه
    output_directory = wordpress_url  # نام دایرکتوری خروجی

    start_post = 1
    while True:
        success = get_wordpress_posts(wordpress_url, wordpress_username,
                                      wordpress_password, start_post,
                                      batch_size, output_directory)
        if not success:
            break
        start_post += batch_size
