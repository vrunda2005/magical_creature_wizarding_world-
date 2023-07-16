from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,Length,EqualTo,DataRequired,ValidationError
from Dumble.model import UserInfo


class RegisterForm(FlaskForm):

    def validate_username(self,username_check):
        user=UserInfo.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError('Username already exists please use another! ')
        
    def validate_email(self,email_check):
        email=UserInfo.query.filter_by(email_address=email_check.data).first()
        if email:
            raise ValidationError('Email already exists please use another!')




    username=StringField(label='User Name',validators=[Length(min=3,max=30),DataRequired()])
    email=StringField(label='Email',validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username=StringField(label='User Name',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='Sign In')