from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery as _BaseQuery
from contextlib import contextmanager

from app.api.v1.libs.error import ResourcesException


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class BaseQuery(_BaseQuery):
    def filter_by(self, o=True, **kwargs):
        if o is True:
            if 'status' not in kwargs.keys():
                kwargs['status'] = 1
        return super(BaseQuery, self).filter_by(**kwargs)

    def get_or_404(self, ident, value=None):

        rv = self.get(ident)
        if rv is None:
            errors = dict()
            errors['model_' + self.column_descriptions[0]['name']] = ['this resource is not found']
            raise ResourcesException(error=errors)
        return rv

    def first_or_404(self):

        rv = self.first()
        if rv is None:
            errors = dict()
            errors['model_' + self.column_descriptions[0]['name']] = ['this resource is not found']
            raise ResourcesException(error=errors)
        return rv


db = SQLAlchemy(query_class=BaseQuery)
