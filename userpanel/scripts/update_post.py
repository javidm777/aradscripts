import os
from xmlrpc.client import ServerProxy


def update_post_content(wordpress_url, username, password, post_id, content,
                        publish=False):
    server = ServerProxy(wordpress_url)
    post_data = {
        'description': content,
        'post_status': 'publish' if publish else 'draft'
    }
    result = server.metaWeblog.editPost(post_id, username, password, post_data)
    return result
