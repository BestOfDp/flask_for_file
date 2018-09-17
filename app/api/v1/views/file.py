from flask import request, g, jsonify

from app.libs.redprint import Redprint
from app.api.v1.libs.token_auth import auth
from app.api.v1.libs.success import AddSuccess, UpdateSuccess, SelectSuccess
from app.api.v1.validate.file import UpdateTitleForm, UploadFileForm, DeleteFileForm, \
    RecoverFileForm, PublicForm
from app.api.v1.libs.decorate import file_user_auth

api = Redprint('file')


@api.route('/upload_file/', methods=['POST'])
@auth.login_required
def upload_file():
    public = request.headers['public']
    file = request.files['file']
    form = UploadFileForm(data=dict(filename=file.filename, public=int(public))).validate_for_api()
    form.save_file(file)
    return AddSuccess(description='file upload success')


@api.route('/update_title/', methods=['POST'])
@auth.login_required
@file_user_auth
def update_title():
    data = request.json
    form = UpdateTitleForm(data=data).validate_for_api()
    form.update_title()
    # 权限 加 装饰器
    return UpdateSuccess(description="file's title update success")


@api.route('/', methods=['DELETE'])
@auth.login_required
@file_user_auth
def delete_file():
    data = request.json
    form = DeleteFileForm(data=data).validate_for_api()
    form.delete_file()
    return UpdateSuccess(description='file delete success')


@api.route('/recover/', methods=['POST'])
@auth.login_required
@file_user_auth
def recover_file():
    data = request.json
    form = RecoverFileForm(data=data).validate_for_api()
    form.recover_file()
    return UpdateSuccess(description='file recover success')


@api.route('/', methods=['POST'])
@auth.login_required
def get_file():
    data = request.json
    form = PublicForm(data=data).validate_for_api()
    data = form.get_files()
    return SelectSuccess(data=data)
