from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import BlogType, BlogPost, BlogComt

#-----------Jack Blog Form
#--------------------------TYPE------------------------------------------------------------

class AddBlogTypeForm(FlaskForm):
    addtype = TextAreaField(('Type Name'),validators=[Length(max=50), DataRequired()])
    submit = SubmitField(('Submit'))


class EditBlogTypeForm(FlaskForm):
    type_id = SelectField('Type', choices=[], validators=[DataRequired()])
    updtype = TextAreaField(('Rename/'),validators=[Length(max=50), DataRequired()])
    delete = SubmitField('Delete')
    submit = SubmitField('Submit')  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_id.choices = [(blogtype.id, blogtype.type) for blogtype in BlogType.query.all()]

#--------------------------POST-----------------------------------------------

class AddBlogPostForm(FlaskForm):
    title = TextAreaField(('Tittle'),validators=[Length(max=50), DataRequired()])
    dct = TextAreaField(('Description'),
                         validators=[Length(max=600), DataRequired()])
    type_id = SelectField('Type', choices=[], validators=[DataRequired()])
    submit = SubmitField(('Submit'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_id.choices = [(blogtype.id, blogtype.type) for blogtype in BlogType.query.all()]


class EditBlogPostForm(FlaskForm):
    title = TextAreaField('Title', validators=[Length(max=50), DataRequired()])
    desc = TextAreaField('Description', validators=[Length(max=600), DataRequired()])
    delete = SubmitField('Delete')
    submit = SubmitField('Update')

#--------------------------Comt---------------------------------------------------------

class AddPostComtForm(FlaskForm):
    content = TextAreaField('Description', validators=[Length(max=100), DataRequired()])
    submit = SubmitField(('Submit'))


class DelComtForm(FlaskForm):
    comts = SelectField('Comments', choices=[], validators=[DataRequired()])
    delete = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comts.choices = [(blogcomt.id, blogcomt.content) for blogcomt in BlogComt.query.all()]
        