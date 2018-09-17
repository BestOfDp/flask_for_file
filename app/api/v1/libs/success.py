from app.api.v1.libs.error import APIException


class RegisterSuccess(APIException):
    status = 200
    detail = 2
    description = 'register success'


class LoginSuccess(APIException):
    status = 200
    detail = 1
    description = 'login success'


class SelectSuccess(APIException):
    status = 200
    detail = 3
    description = 'select success'


class UpdateSuccess(APIException):
    status = 200
    detail = 4
    description = 'update success'


class AddSuccess(APIException):
    status = 200
    detail = 5
    description = 'add success'


class DeleteSuccess(APIException):
    status = 200
    detail = 6
    description = 'delete success'
