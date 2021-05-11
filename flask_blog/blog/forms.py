from flask_wtf import FlaskForm
from flask_wtf.file import (
	FileField, 
	FileAllowed
)
from wtforms import (
	StringField, 
	TextAreaField,
	PasswordField, 
	SubmitField, 
	BooleanField
)
from wtforms.validators import (
	DataRequired, 
	Length, 
	Email, 
	EqualTo,
	ValidationError
)
from blog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
	username = StringField(
		'Username', 
		validators=[
			DataRequired(),
			Length(min=2, max=20)
		]
	)
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	password = PasswordField(
		'Password',
		validators=[
			DataRequired()
		]
	)
	confirm_password = PasswordField(
		'Confirm password',
		validators=[
			DataRequired(),
			EqualTo('password')
		]
	)
	submit = SubmitField('Sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('User with such a username already exists!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('User with such an email already exists!')


class LoginForm(FlaskForm):
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	password = PasswordField(
		'Password',
		validators=[
			DataRequired()
		]
	)
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
	username = StringField(
		'Username', 
		validators=[
			DataRequired(),
			Length(min=2, max=20)
		]
	)
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
	submit = SubmitField('Save')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('User with such a username already exists!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('User with such an email already exists!')


class CreatePostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=100)])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Create') 

	def validate_title(self, title):
		if len(title.data) > 100:
			raise ValidationError('Title cannot have more than 100 symbols!')


class UpdatePostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=100)])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Update') 

	def validate_title(self, title):
		if len(title.data) > 100:
			raise ValidationError('Title cannot have more than 100 symbols!')


class DeletePostForm(FlaskForm):
	submit = SubmitField('Yes, delete')