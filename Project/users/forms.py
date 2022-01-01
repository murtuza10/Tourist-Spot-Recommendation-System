from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,SelectField
from wtforms.validators import DataRequired, Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField , FileAllowed

from flask_login import current_user
from Project.models import User


class UserLoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class UserRegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    dob = DateField('Date of Birth',validators=[DataRequired()])
    gender = SelectField('Gender',choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    picture = FileField('Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Signup')


    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')
