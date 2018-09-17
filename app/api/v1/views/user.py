from flask import request, jsonify, g, current_app
from flask_mail import Message

from app.libs.redprint import Redprint
from app.api.v1.libs.success import RegisterSuccess, LoginSuccess, SelectSuccess, UpdateSuccess
from app.api.v1.validate.user import RegisterForm, LoginForm, NameForm, \
    EmailForm, ImageForm, UpdatePasswordForm, UserAuthFrom
from app.models.user import User
from app.api.v1.libs.token_auth import auth
from app.db import db

api = Redprint('user')


@api.route('/register/', methods=['POST'])
def register_user():
    data = request.json
    form = RegisterForm(data=data).validate_for_api()
    form.register()
    return RegisterSuccess()


@api.route('/login/', methods=['POST'])
def login():
    data = request.json
    form = LoginForm(data=data).validate_for_api()
    data = form.get_user_info()
    return LoginSuccess(data=data)


@api.route('/update_name/', methods=['POST'])
@auth.login_required
def update_name():
    data = request.json
    form = NameForm(data=data).validate_for_api()
    with db.auto_commit():
        user = User.query.filter_by(id=g.user.id).first_or_404()
        user.name = form.data['name']
    return UpdateSuccess(description="user's name has update")


@api.route('/update_email/', methods=['POST'])
@auth.login_required
def update_email():
    data = request.json
    form = EmailForm(data=data).validate_for_api()
    form.update_email()
    return UpdateSuccess(description="user's email has update")


@api.route('/update_image/', methods=['POST'])
@auth.login_required
def update_image():
    file = request.files['file']
    form = ImageForm(data=dict(filename=file.filename)).validate_for_api()
    form.update_image(file)
    return UpdateSuccess(description="user's head_image has update")


@api.route('/update_password/', methods=['POST'])
@auth.login_required
def update_password():
    data = request.json
    UpdatePasswordForm(data=data).validate_for_api()
    # form.update_password()
    return UpdateSuccess(description="user's password has update")


@api.route('/all_user/', methods=['GET'])
@auth.login_required
def all_user():
    users = User.query.filter_by().order_by('id').all()
    resl = jsonify(users).json
    # from collections import OrderedDict
    # data = OrderedDict()
    # for o in resl:
    #     data[o['name']] = o
    return SelectSuccess(data=resl)


@api.route('/', methods=['GET'])
@auth.login_required
def get_user():
    user = User.query.filter_by(id=g.user.id).first_or_404()
    data = jsonify(user).json
    return SelectSuccess(data=data)


@api.route('/auth/', methods=['POST'])
@auth.login_required
def auth():
    data = request.json
    form = UserAuthFrom(data=data).validate_for_api()
    return UpdateSuccess(description='user has been ordinary') if form.update_auth() else UpdateSuccess(
        description='user has been admin')


@api.route('/send_email/', methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        from app import mail
        info = eval(str(request.data, encoding='utf-8'))
        msg = info['msg']
        title = info['title']
        to = info['to']

        msg = Message(title,
                      sender=current_app.config['MAIL_USERNAME'],
                      body=msg,
                      recipients=[to])
        mail.send(msg)
        return "YES"
    return "YES"
