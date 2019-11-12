from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired
import config



# class ContainerSetupForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     submit = SubmitField('Submit')

class CategorySetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LinkSetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])
    submit = SubmitField('Submit')
