from flask import (
	render_template, 
	url_for, 
	flash, 
	redirect,
	request
)
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from flask_login import (
	login_user, 
	logout_user, 
	current_user, 
	login_required
)


@app.route('/')
def home():
	title = 'Blog | Home page'
	return render_template('home.html', title=title)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	title = 'Blog | Register'
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
		user = User(
			username=form.username.data,
			email=form.email.data,
			password=hashed_password
		)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title=title, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	title = 'Blog | Login'
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				next_page = request.args.get('next')
				if next_page:
					return redirect(next_page)
				flash(f'Welcome to Home page!', 'success')
				return redirect(url_for('home'))
			else:
				flash('Invalid username or password', 'danger')
		else:
			flash(f'Such user does not exist!', 'danger')
	return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
	logout_user()
	title = 'Blog | Log out'
	return render_template('logout.html', title=title)

@app.route('/account')
@login_required
def account():
	title = 'Blog | Your account'
	return render_template('account.html', title=title)