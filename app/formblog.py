from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import BlogType


class AddBlogTypeForm(FlaskForm):
    bigtype = TextAreaField(('Type Name'),validators=[Length(max=50), DataRequired()])
    submit = SubmitField(('Submit'))


class AddBlogPostForm(FlaskForm):
    title = TextAreaField(('Tittle'),validators=[Length(max=50), DataRequired()])
    desc = TextAreaField(('Description'),
                         validators=[Length(max=600), DataRequired()])
    type = SelectField('Type', choices=[], validators=[DataRequired()])
    submit = SubmitField(('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = [(BlogType.id, BlogType.type) for BlogType in BlogType.query.all()]



class EditBlogPostForm(FlaskForm):
    title = TextAreaField('Title', validators=[Length(max=50), DataRequired()])
    desc = TextAreaField('Description', validators=[Length(max=600), DataRequired()])
    delete = SubmitField('Delete')
    submit = SubmitField('Update')