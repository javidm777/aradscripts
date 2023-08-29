# wordpress_script.py

import os
from xmlrpc.client import ServerProxy


def update_post_content(wordpress_url, username, password, post_id, content,
                        publish=False):
    server = ServerProxy(wordpress_url + '/xmlrpc.php')
    post_data = {
        'description': content,
        'post_status': 'publish' if publish else 'draft'
    }
    result = server.metaWeblog.editPost(post_id, username, password, post_data)
    print(result)
    return result


def run_wordpress_update_script(content_folder, wordpress_url, username,
                                password):
    for filename in os.listdir(content_folder):
        if filename.endswith('.txt'):
            post_id = filename[:-4]
            with open(os.path.join(content_folder, filename), 'r',
                      encoding='utf-8') as file:
                content = file.read()
                update_result = update_post_content(wordpress_url, username,
                                                    password, post_id, content,
                                                    publish=True)
                if update_result:
                    print(f"Post {post_id} updated and published successfully.")
                else:
                    print(f"Failed to update and publish post {post_id}.")
