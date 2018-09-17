from wtforms.validators import ValidationError
from app.api.v1.validate.base import Base, StringField, DataRequired
from app.models.blog import Blog
from app.libs.save_md import save_md
from app.db import db


class AddBlogForm(Base):
    title = StringField(validators=[
        DataRequired('标题不能为空')
    ])
    md = StringField(validators=[
        DataRequired('文本信息不能为空')
    ])

    def validate_title(self, value):
        blog = Blog.query.filter_by(title=value.data).first()
        if blog:
            raise ValidationError(description='标题已存在')

    def add_md(self):
        path = save_md(self.md.data)
        with db.auto_commit():
            blog = Blog(
                title=self.title.data,
                watched=0,
                md_path=path
            )
            db.session.add(blog)
