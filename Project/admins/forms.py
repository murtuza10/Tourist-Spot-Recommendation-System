from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,SelectField
from wtforms.validators import DataRequired, Email,EqualTo
from wtforms import ValidationError
from Project.models import Admin


class AdminLoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminRegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Signup')


    def validate_email(self, email):
        if Admin.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')
    def validate_username(self, username):
        if Admin.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')
