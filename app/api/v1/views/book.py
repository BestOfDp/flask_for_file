from flask import request, jsonify, g

from app.libs.redprint import Redprint
from app.api.v1.libs.token_auth import auth
from app.api.v1.validate.book import SearchBookForm, OrderBookForm
from app.api.v1.libs.success import SelectSuccess, UpdateSuccess
from app.models.subscribe import Subscribe

api = Redprint('book')


@api.route('/', methods=['POST'])
@auth.login_required
def search_books():
    data = request.json
    form = SearchBookForm(data=data).validate_for_api()
    data = form.search()
    return SelectSuccess(data=data)


@api.route('/', methods=['GET'])
@auth.login_required
def get_order_book():
    books = Subscribe.query.filter_by(
        o=False, owner_id=g.user.id
    ).order_by(
        Subscribe.create_time.desc()
    ).all()
    return SelectSuccess(data=jsonify(books).json)


@api.route('/order/', methods=['POST'])
@auth.login_required
def order_book():
    data = request.json
    form = OrderBookForm(data=data).validate_for_api()
    form.save_or_cancel()
    return UpdateSuccess(
        description='order book success'
    ) if form.type.data == 1 else UpdateSuccess(
        description='cancel book success')
