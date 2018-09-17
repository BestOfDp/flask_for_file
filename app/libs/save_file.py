import os
import uuid
from flask import current_app

from app.api.v1.libs.enum import SaveFileEnum
from app.db import db
from app.models.file import File
from app.libs.spilt_point import spilt_point


def makedir(url):
    if not os.path.exists(url):
        os.makedirs(url)


def get_file_url(type):
    return os.path.dirname(os.path.dirname(__file__)) + current_app.config[type]


def _save_image(user, filename, file, public, replace=True):
    url = get_file_url('HEAD_IMAGE_URL')
    makedir(url)
    title, tail = spilt_point(filename)
    if user.photo_url != current_app.config['DEFAULT_IMAGE'] and replace:
        os.remove(url + user.photo_url)

    new_url = uuid.uuid1().hex + '.' + tail
    file_url = url + new_url
    file.save(file_url)
    with db.auto_commit():
        user.photo_url = new_url


def _save_file(user, filename, file, public):
    title, tail = spilt_point(filename)
    url = get_file_url('USER_FILE_URL') + str(user.id) + '/' + tail + '/'
    makedir(url)
    url = url + uuid.uuid1().hex + '.' + tail
    file.save(url)
    with db.auto_commit():
        new_file = File(
            title=title,
            format=tail,
            owner_id=user.id,
            all_could=public,
            url=url.replace(get_file_url('USER_FILE_URL'), '')
        )
        db.session.add(new_file)


def save(user, filename, file, type, public, replace=True):
    """
    :param user: 用户
    :param filename: 标题
    :param file: 文件
    :param replace: 为True时，删除旧地址的文件
    :param type: 类型
    :return:
    """
    promise = {
        SaveFileEnum.IMAGE.name: _save_image,
        SaveFileEnum.FILE.name: _save_file
    }
    promise[SaveFileEnum(type).name](user, filename, file, public)
    pass
