from flask import current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from app.api.v1.libs.error import AuthException

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    user = token_detail(token)
    if user:
        g.user = user
        return True
    else:
        return False


def token_detail(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # from flask import request
        # data = request
        data = s.loads(token)
    except SignatureExpired:
        raise AuthException(error=dict(token=['登录验证过期']))
    except BadSignature:
        raise AuthException(error=dict(token=['登录验证失败']))

    from collections import namedtuple
    User = namedtuple('User', ['id', 'password'])
    user = User(data['uid'], data['password'])
    return user
