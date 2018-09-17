from wtforms.validators import NumberRange, ValidationError
from flask import jsonify, g

from app.api.v1.validate.base import Base, StringField, Length, DataRequired, IntegerField
from app.models.books import Books
from app.models.subscribe import Subscribe
from sqlalchemy import or_
from app.db import db


class SearchBookForm(Base):
    keyword = StringField(validators=[
        DataRequired('关键字不能为空'),
        Length(max=20, message='关键字长度不能超过20')
    ])

    def search(self):
        books = Books.query.filter(
            or_(Books.title.ilike("%" + self.keyword.data + "%"), \
                Books.author.ilike("%" + self.keyword.data + "%"), )
        ).order_by(Books.id.asc()).all()
        data = jsonify(books).json
        return data


class OrderBookForm(Base):
    bid = IntegerField(validators=[
        DataRequired('书籍编号不能为空'),
        NumberRange(min=1, message='书籍编号需要为正整数'),
    ])
    type = IntegerField(validators=[
        DataRequired('请选择订阅(1)或取消(0)'),
        NumberRange(min=0, max=1, message='请选择订阅(1)或取消(0)')
    ])

    def validate_bid(self, value):
        Books.query.filter_by(id=value.data).first_or_404()

    def validate_type(self, value):
        if value.data == 1 and self.judge_order():
            raise ValidationError(message='你已经订阅此书')
        elif value.data == 0 and not self.judge_order():
            raise ValidationError(message='你没有订阅此书')

    def judge_order(self):
        sub = Subscribe.query.filter_by(book_id=self.bid.data, owner_id=g.user.id).first()
        return True if sub else False

    def save_or_cancel(self):
        with db.auto_commit():
            if self.type.data == 1:
                info = Subscribe(
                    owner_id=g.user.id,
                    book_id=self.bid.data
                )
                db.session.add(info)
            else:
                sub = Subscribe.query.filter_by(
                    owner_id=g.user.id, book_id=self.bid.data
                ).first_or_404()
                db.session.delete(sub)
