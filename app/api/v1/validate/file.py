from flask import g, jsonify
from wtforms import IntegerField
from wtforms.validators import NumberRange, ValidationError

from app.api.v1.validate.base import Base
from app.api.v1.validate.base import StringField, Length, DataRequired
from app.models.file import File
from app.models.user import User
from app.api.v1.libs.enum import FilePublicAuthEnum, SaveFileEnum
from app.libs.spilt_point import spilt_point
from app.api.v1.libs.enum import StatusEnum
from app.api.v1.libs.error import ParameterException
from app.db import db
from sqlalchemy import or_
from datetime import datetime


class FileIDForm(Base):
    file_id = IntegerField(validators=[
        DataRequired('文件编号不能为空'),
        NumberRange(min=1, message='文件编号不能小于1')
    ])

    def validate_file_id(self, value):
        file = File.query.filter_by(o=False, id=value.data).first()
        if not file:
            raise ValidationError(message='file is not exist')
        else:
            if file.status == StatusEnum.DELETE.value:
                raise ValidationError(message='file has been deleted')


class PublicForm(Base):
    public = IntegerField(validators=[
        DataRequired('请选择是否公共'),
        NumberRange(min=1, max=3, message='public must 1(public) or 2(private) and 3(delete)')
    ])

    def get_files(self):
        promise = {
            FilePublicAuthEnum.PUBLIC.name: self._public_file,
            FilePublicAuthEnum.PRIVATE.name: self._private_file,
            FilePublicAuthEnum.DELETED.name: self._deleted_file
        }
        return promise[FilePublicAuthEnum(self.public.data).name]()

    @staticmethod
    def _get_resl(files):
        resl = []
        for file in files:
            data = jsonify(file).json
            data['username'] = file.owner.name
            data['filename'] = data['title'] + '.' + data['format']
            data['user_auth'] = file.owner.auth
            resl.append(data)
        return resl

    def _public_file(self):
        files = File.query.filter_by(all_could=True).order_by(File.create_time.desc()).all()
        return self._get_resl(files)

    def _private_file(self):
        files = File.query.filter_by(owner_id=g.user.id, all_could=False).order_by(File.create_time.desc()).all()
        return self._get_resl(files)

    def _deleted_file(self):
        user = User.query.get_or_404(g.user.id)
        user_auth = user.auth
        files = File.query.join(
            User
        ).filter(
            File.status == 0,
            or_(File.owner_id == g.user.id, User.auth < user_auth)
        ).order_by(File.del_time.desc()).all()
        return self._get_resl(files)


class UploadFileForm(PublicForm):
    filename = StringField(validators=[
        DataRequired('文件名不能为空'),
        Length(max=100, message='文件名长度不能超过20')
    ])

    def validate_filename(self, value):
        title, tail = spilt_point(value.data)
        file = File.query.filter_by(o=False, title=title, owner_id=g.user.id).first()
        if file:
            raise ValidationError(message='filename is exist')

    def save_file(self, file):
        user = User.query.filter_by(id=g.user.id).first_or_404()
        public = True if self.public.data == FilePublicAuthEnum.PUBLIC.value else False
        user.save_file(self.filename.data, file, type=SaveFileEnum.FILE.value, public=public)


class UpdateTitleForm(FileIDForm):
    title = StringField(validators=[
        DataRequired('文件名不能为空'),
        Length(max=100, message='文件名长度不能超过20')
    ])

    def validate_title(self, value):
        file = File.query.filter_by(o=False, title=value.data).first()
        if file:
            raise ValidationError(message='filename is exist')

    def update_title(self):
        file = File.query.filter_by(id=self.file_id.data).first_or_404()
        with db.auto_commit():
            file.title = self.title.data


class DeleteFileForm(FileIDForm):
    def delete_file(self):
        file = File.query.filter_by(id=self.file_id.data).first_or_404()
        with db.auto_commit():
            file.del_time = datetime.now()
            file.status = StatusEnum.DELETE.value


class RecoverFileForm(FileIDForm):
    def validate_file_id(self, value):
        file = File.query.filter_by(o=False, id=value.data).first()
        if not file:
            raise ValidationError(message='file is not exist')
        else:
            if file.status == StatusEnum.NORMAL.value:
                raise ValidationError(message='file has not been deleted')

    def recover_file(self):
        file = File.query.filter_by(id=self.file_id.data, status=StatusEnum.DELETE.value).first_or_404()
        with db.auto_commit():
            file.status = StatusEnum.NORMAL.value
