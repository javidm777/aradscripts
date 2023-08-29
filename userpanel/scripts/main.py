import xmlrpc.client
from userpanel.models import ContentWebsite


def get_wordpress_posts(wp_url, wp_username, wp_password, start_post,
                        batch_size, website_id):
    server = xmlrpc.client.ServerProxy(wp_url + '/xmlrpc.php')

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
                ContentWebsite.objects.create(
                    website_id= website_id,
                    post_id=post['post_id'],
                    title=post['post_title'],
                    content=post['post_content'],
                )

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            retries += 1

    return False

