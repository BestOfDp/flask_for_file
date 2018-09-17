from flask import Blueprint


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    from app.api.v1.views import user, file, book, blog
    user.api.register(bp_v1, url_prefix='user')
    file.api.register(bp_v1, url_prefix='file')
    book.api.register(bp_v1, url_prefix='book')
    blog.api.register(bp_v1, url_prefix='blog')
    return bp_v1
