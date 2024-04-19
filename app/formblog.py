from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, Blogger, BlogPost



class AddBlogPostForm(FlaskForm):
    title = TextAreaField(('Tittle'),validators=[Length(max=50), DataRequired()])
    desc = TextAreaField(('BlogPost Description'),
                         validators=[Length(max=600), DataRequired()])
    author_id = SelectField('author', choices=[], validators=[DataRequired()])
    submit = SubmitField(('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [(Blogger.id, Blogger.name) for Blogger in Blogger.query.all()]

