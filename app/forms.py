from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, RadioField, DecimalField, FieldList, IntegerField, FormField, \
    FloatField
from wtforms.fields.html5 import DateField 
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, NumberRange, Optional
from app.models import User, Category, Link
from werkzeug.datastructures import MultiDict
import config

def object_troubleshoot(obj):

    for attr in dir(obj):
        try:
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
        except:
            pass



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LinkSetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    submit = SubmitField('Complete')


class LinkModificationSubForm(FlaskForm):
    name = StringField('Name', validators=[Optional()], filters=[lambda x: x or None])
    url = StringField('Url', validators=[Optional()], filters=[lambda x: x or None])


class LinkModificationForm(FlaskForm):
    links = FieldList(FormField(LinkModificationSubForm))
    submit = SubmitField('Complete')

    def populate_form(category_id):
        links = Link.query.filter_by(category_id=category_id).all()
        link_form = LinkModificationForm()
        while len(link_form.links) > 0:
            link_form.links.pop_entry()
        for link in links:
            l_data = dict()
            l_data['name'] = link.name
            l_data['url'] = link.url
            link_form.links.append_entry(l_data)
            
        return link_form


class CategorySetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Complete')


class WarningForm(FlaskForm ):
    delete = SubmitField('Delete Catgory')
    save = SubmitField('Return')








#**************** Extra Code ***************************************


class EditProfileForm(FlaskForm):
    '''
    The implementation is in a custom validation method, but there is an overloaded 
    constructor that accepts the original username as an argument. This username is 
    saved as an instance variable, and checked in the validate_username() method. If 
    the username entered in the form is the same as the original username, then there 
    is no reason to check the database for duplicates.

    To use this new validation method, I need to add the original username argument 
    in the view function, where the form object is created:
    '''
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1,max=140)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')