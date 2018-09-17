from flask import current_app, g, jsonify
from app.api.v1.validate.base import StringField, IntegerField
from wtforms.validators import Email, ValidationError

from app.api.v1.validate.base import Base
from app.api.v1.validate.base import Length, NumberRange, DataRequired
from app.api.v1.libs.error import ParameterException
from app.models.user import User
from app.db import db
from app.libs.spilt_point import spilt_point
from app.api.v1.libs.enum import SaveFileEnum


class NameForm(Base):
    name = StringField(validators=[
        DataRequired('用户名不能为空'),
        Length(min=3, max=11, message='用户名长度需要在[3,11]之间')
    ])

    def validate_name(self, value):
        if User.check_new_name(value.data):
            raise ValidationError(message='用户名已存在')


class EmailForm(Base):
    email = StringField(validators=[
        DataRequired('邮箱不能为空'),
        Email(message='邮箱格式不正确')
    ])

    def update_email(self):
        with db.auto_commit():
            user = User.query.filter_by(id=g.user.id).first_or_404()
            user.email = self.email.data


class UserForm(Base):
    password = StringField(validators=[
        DataRequired('密码不能为空'),
        Length(min=6, max=20, message='密码长度需要在[6,20]之间')
    ])
    name = StringField(validators=[
        DataRequired('用户名不能为空'),
        Length(min=3, max=11, message='用户名长度需要在[3,11]之间')
    ])


class LoginForm(UserForm):

    def validate_name(self, value):
        user = User.query.filter_by(name=value.data).first_or_404()
        if 'password' not in self.errors.keys():
            if not user:
                raise ValidationError(message='用户名不存在或密码错误')
            else:
                if not user.check_pwd(self.password.data):
                    raise ValidationError(message='用户名不存在或密码错误')

    def get_user_info(self):
        user = User.query.filter_by(name=self.name.data).first_or_404()
        token = user.get_auth_token(password=self.password.data)
        data = jsonify(user).json
        print(data)
        data['token'] = token
        data['expires'] = current_app.config['EXPIRES_IN']
        return data

    # def validate_password(self, value):
    #     user = User.query.filter_by(name=self.name.data).first()
    #     if user:
    #         if not user.check_pwd(value.data):
    #             raise ValidationError(message='用户名不存在或密码错误')


class ImageForm(Base):
    filename = StringField(validators=[
        DataRequired('文件名不能为空'),
    ])

    def validate_filename(self, value):
        title, tail = spilt_point(value.data)
        # self.filename = self.filename.lower()
        if str(tail).lower() not in current_app.config['HEAD_IMAGE']:
            raise ParameterException(error=dict(filename=['图片格式不正确']))
        self.filename.data = self.filename.data.lower()
        self.filename.title = title
        self.filename.tail = str(tail).lower()

    def update_image(self, file):
        user = User.query.get_or_404(g.user.id)
        user.save_file(self.filename.data, file, type=SaveFileEnum.IMAGE)


class RegisterForm(UserForm):
    class_name = StringField(validators=[DataRequired('班级不能为空')])
    email = StringField(validators=[Email('邮箱格式不正确')])
    re_password = StringField(validators=[
        DataRequired('请重复密码'),
        Length(min=6, max=20, message='新密码长度需要在[6,20]之间')
    ])

    def validate_name(self, value):
        user = User.query.filter_by(False, name=value.data).first()
        if user:
            raise ValidationError(message='用户名已被注册')

    def validate_re_password(self, value):
        if 'password' not in self.errors.keys():
            if self.password.data != value.data:
                raise ValidationError(message='与密码不一致')

    def register(self):
        with db.auto_commit():
            user = User(
                name=self.name.data,
                password=self.password.data,
                class_name=self.class_name.data,
                email=self.email.data
            )
            db.session.add(user)


class UpdatePasswordForm(Base):
    """
    旧 新 重复新
    """
    new_password = StringField(validators=[
        DataRequired('新密码不能为空'),
        Length(min=6, max=20, message='新密码长度需要在[6,20]之间')
    ])
    re_password = StringField(validators=[
        DataRequired('请重复密码'),
        Length(min=6, max=20, message='新密码长度需要在[6,20]之间')
    ])
    old_password = StringField(validators=[
        DataRequired('原密码不能为空'),
        Length(min=6, max=20, message='原密码长度需要在[6,20]之间')
    ])

    def validate_old_password(self, value):
        user = User.query.filter_by(id=g.user.id).first_or_404()
        if user.check_pwd(value.data):
            with db.auto_commit():
                user.password = self.new_password.data
        else:
            if 'new_password' not in self.errors.keys() and 're_password' not in self.errors.keys():
                raise ValidationError(message='原密码错误')

    def validate_re_password(self, value):
        if 'new_password' not in self.errors.keys():
            if self.new_password.data != value.data:
                raise ValidationError(message='与新密码不一致')

    def update_password(self):
        user = User.query.get(g.user.id)
        with db.auto_commit():
            user.password = self.new_password.data


class UserAuthFrom(Base):
    uid = IntegerField(validators=[
        DataRequired('类型不能为空'),
        NumberRange(min=1, message='用户ID必须大于0 ')
    ])
    type = IntegerField(validators=[
        DataRequired('类型不能为空'),
        NumberRange(min=0, max=1, message='type must 0(ordinary) or 1(admin)')
    ])

    def validate_type(self, value):
        if not self.errors:
            user = User.query.filter_by(id=self.uid.data).first_or_404()
            setattr(self, 'user', user)
            if user.auth == value.data:
                raise ValidationError(message='Maybe he was before.')

    def update_auth(self):
        with db.auto_commit():
            self.user.auth = self.type.data
        return True if self.type.data == 1 else False
