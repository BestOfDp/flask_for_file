from flask import current_app, g, request
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models.user import User
from app.models.file import File
from app.api.v1.libs.error import AuthException


def blog_for_1ni(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.id != 1:
            return AuthException(description='你没有关于博客的权限')
        return f(*args, **kwargs)

    return decorated_function


def check_user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        s = Serializer(current_app.config['SECRET_KEY'])
        token = request.environ['HTTP_AUTHORIZATION'].split(' ')[1]
        s.loads(token)

        return f(*args, **kwargs)

    return decorated_function


def file_user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.get_or_404(g.user.id)
        user_auth = user.auth
        file = File.query.get_or_404(request.json['file_id'])
        file_auth = file.owner.auth
        if (user_auth <= file_auth or file.all_could == 0) and g.user.id != file.owner_id:
            return AuthException(error=dict(auth=['你没有权限操作别人的文件']))
        return f(*args, **kwargs)

    return decorated_function
