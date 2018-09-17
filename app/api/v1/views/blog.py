from flask import request, jsonify
from app.libs.redprint import Redprint
from app.api.v1.libs.token_auth import auth
from app.api.v1.validate.blog import AddBlogForm
from app.api.v1.libs.decorate import blog_for_1ni
from app.api.v1.libs.success import AddSuccess, SelectSuccess
from app.models.blog import Blog

api = Redprint('blog')


@api.route('/', methods=['GET'])
def get_blog():
    blogs = Blog.query.filter_by().all()
    data = jsonify(blogs).json
    return SelectSuccess(data=data)


@api.route('/', methods=['POST'])
@auth.login_required
@blog_for_1ni
def add_blog():
    data = request.json
    form = AddBlogForm(data=data).validate_for_api()
    form.add_md()
    return AddSuccess()
