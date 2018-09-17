import uuid
import os
from flask import current_app


def save_md(md):
    md_path = uuid.uuid1().hex
    path = os.path.dirname(os.path.dirname(__file__)) + current_app.config['BLOG_MD_URL'] + md_path + '.md'
    with open(path, 'w') as fp:
        fp.write(md)
    return md_path
