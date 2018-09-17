from wtforms import Form
from wtforms.validators import StopValidation
from wtforms.validators import Length as _Length
from wtforms.validators import NumberRange as _NumberRange
from wtforms.validators import DataRequired as _DataRequired
from wtforms import Field as _Field

from app.api.v1.libs.error import ParameterException
from wtforms import widgets
from wtforms.compat import text_type

__all__ = (
    'StringField', 'Length', 'Base', 'NumberRange', 'IntegerField', 'DataRequired'
)


class Field(_Field):
    def _run_validation_chain(self, form, validators):
        for validator in validators:
            try:
                validator(form, self)
            except StopValidation as e:
                if e.args and e.args[0]:
                    self.errors.append(e.args[0])
                    form.errors[self.name] = self.errors
                return True
            except ValueError as e:
                self.errors.append(e.args[0])
                form.errors[self.name] = self.errors

        return False


class StringField(Field):
    widget = widgets.TextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        else:
            self.data = ''

    def _value(self):
        return text_type(self.data) if self.data is not None else ''


class IntegerField(Field):
    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super(IntegerField, self).__init__(label, validators, **kwargs)

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data is not None:
            return text_type(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid integer value'))


class Length(_Length):
    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext('Field must be at least %(min)d character long.',
                                             'Field must be at least %(min)d characters long.', self.min)
                elif self.min == -1:
                    message = field.ngettext('Field cannot be longer than %(max)d character.',
                                             'Field cannot be longer than %(max)d characters.', self.max)
                else:
                    message = field.gettext('Field must be between %(min)d and %(max)d characters long.')

            raise StopValidation(message % dict(min=self.min, max=self.max, length=l))


class NumberRange(_NumberRange):
    class NumberRange(object):
        def __call__(self, form, field):
            data = field.data
            if data is None or (self.min is not None and data < self.min) or \
                    (self.max is not None and data > self.max):
                message = self.message
                if message is None:
                    # we use %(min)s interpolation to support floats, None, and
                    # Decimals without throwing a formatting exception.
                    if self.max is None:
                        message = field.gettext('Number must be at least %(min)s.')
                    elif self.min is None:
                        message = field.gettext('Number must be at most %(max)s.')
                    else:
                        message = field.gettext('Number must be between %(min)s and %(max)s.')

                raise StopValidation(message % dict(min=self.min, max=self.max))


class Base(Form):
    def validate_for_api(self):
        form = super(Base, self).validate()
        if not form:
            raise ParameterException(error=self.errors)
        else:
            return self


class DataRequired(_DataRequired):
    def __call__(self, form, field):
        if field.data != 0:
            super(DataRequired, self).__call__(form, field)
