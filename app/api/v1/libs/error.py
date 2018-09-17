from werkzeug.exceptions import HTTPException
from flask import json, request


class APIException(HTTPException):
    code = 200
    detail = 0
    status = 500
    description = 'you got wrong'

    def __init__(self, code=None, detail=None, status=None,
                 description=None, error=None, data=None, size=None):
        if size:
            self.size = size
        if code:
            self.code = code
        if status:
            self.status = status
        if detail:
            self.detail = detail
        if description:
            self.description = description
        if error:
            self.error = error
        if data:
            self.data = data
        super(APIException, self).__init__(description)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def get_body(self, environ=None):
        resl = dict(
            status=self.status,
            msg=self.description,
            request_url=self.get_request_url
        )
        if hasattr(self, 'data'):
            resl['data'] = self.data
        if hasattr(self, 'size'):
            resl['size'] = self.size
        if hasattr(self, 'error'):
            resl['error'] = self.error
        if hasattr(self, 'detail'):
            resl['detail'] = self.detail
        resl = json.dumps(resl, sort_keys=False)
        return resl

    @property
    def get_request_url(self):
        data = request.full_path.split('?')
        return data[0]


class ParameterException(APIException):
    status = 400
    description = 'parameter wrong'


class AuthException(APIException):
    status = 401
    description = 'you have not auth to do this'


class ResourcesException(APIException):
    status = 404
    description = 'resources is not found'


class ServerException(APIException):
    status = 500
    description = 'Something wrong'
