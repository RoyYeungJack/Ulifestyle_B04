from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, Blogger, BlogPost , BlogType



class AddBlogPostForm(FlaskForm):
    title = TextAreaField(('Tittle'),validators=[Length(max=50), DataRequired()])
    desc = TextAreaField(('BlogPost Description'),
                         validators=[Length(max=600), DataRequired()])
    type = SelectField('Type', choices=[], validators=[DataRequired()])
    submit = SubmitField(('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = [(BlogType.id, BlogType.type) for BlogType in BlogType.query.all()]

