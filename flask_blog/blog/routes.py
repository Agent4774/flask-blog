from blog import app, db, bcrypt
from blog.models import User, Post
from blog.forms import (
	RegistrationForm, 
	LoginForm, 
	UpdateAccountForm,
	CreatePostForm,
	UpdatePostForm,
	DeletePostForm,
	ChangePasswordForm
)
from blog.utils import save_picture
from flask import (
	render_template, 
	url_for, 
	flash, 
	redirect,
	request
)
from flask_login import (
	login_user, 
	logout_user, 
	current_user, 
	login_required
)
from sqlalchemy import desc


@app.route('/')
def home():
		title = 'Blog | Home page'
		posts = Post.query.order_by(desc('date_posted'))
		return render_template('home.html', title=title, posts=posts)

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
		return render_template('user/register.html', title=title, form=form)

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
							return redirect(url_for('account'))
					else:
						flash('Invalid username or password', 'danger')
			else:
					flash(f'Such user does not exist!', 'danger')
		return render_template('user/login.html', title=title, form=form)

@app.route('/logout')
def logout():
		logout_user()
		title = 'Blog | Log out'
		return render_template('user/logout.html', title=title)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
		title = 'Blog | Your account'
		image_file = url_for(
			'static', 
			filename=f'pictures/{current_user.image_file}'
		)
		form = UpdateAccountForm()
		if form.validate_on_submit():
				if form.username.data != current_user.username \
				or form.email.data != current_user.email \
				or form.picture.data:
					current_user.username = form.username.data
					current_user.email = form.email.data
					current_user.image_file = save_picture(current_user, form.picture.data)
					db.session.commit()
					flash('Your account has been updated!', 'success')
					return redirect(url_for('account'))
		if request.method == 'GET':
				form.username.data = current_user.username
				form.email.data = current_user.email
		return render_template(
			'user/account.html', 
			title=title, 
			image_file=image_file, 
			form=form
		)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
		title = 'Blog | Create post'
		form = CreatePostForm()
		if form.validate_on_submit():
				post = Post(
					title=form.title.data,
					content=form.content.data,
					user_id=current_user.id
				)
				db.session.add(post)
				db.session.commit()
				return redirect(url_for('detail_post', post_id=post.id))
		if request.method == 'GET':
				form.title.data = ''
				form.content.data = ''
		return render_template('post/create_post.html', title=title, form=form)

@app.route('/post/<post_id>')
@login_required
def detail_post(post_id):
		post = Post.query.get(post_id)
		title = f'Blog | {post.title.capitalize()}'
		return render_template('post/detail_post.html', title=title, post=post)

@app.route('/post/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
		post = Post.query.get(post_id)
		if current_user == post.author: 
				title = f'Blog | Update "{post.title.capitalize()}"'
				form = UpdatePostForm()
				if form.validate_on_submit():
						if post.title != form.title.data \
						or post.content != form.content.data:
								post.title = form.title.data
								post.content = form.content.data
								db.session.commit()
								flash('Post has been updated!', 'success')
						return redirect(url_for('detail_post', post_id=post.id))
				if request.method == 'GET':
						form.title.data = post.title
						form.content.data = post.content
				return render_template(
					'post/update_post.html', 
					title=title, 
					post=post, 
					form=form
				)
		title = 'Access denied!'
		return render_template('access_denied.html', title=title)

@app.route('/post/delete/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
		post = Post.query.get(post_id)
		if current_user == post.author:
				if request.method == 'GET':
						form = DeletePostForm()
						title = 'Blog | Confirm deletion'
						return render_template(
							'post/delete_post.html', 
							post=post, 
							form=form
						)
				# Deleting a post on POST request
				flash(f'Post "{post.title.capitalize()}" has been deleted!') 
				db.session.delete(post)
				db.session.commit()
				return redirect(url_for('home'))
		title = 'Access denied!'
		return render_template('access_denied.html', title=title)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
		title = 'Blog | Change password'
		form = ChangePasswordForm()
		if form.validate_on_submit():
				hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode()
				current_user.password = hashed_password
				db.session.commit()
				flash('Your password has been changed!', 'success')
				return redirect('account')
		if request.method == 'GET':
				form.old_password.data = ''
				form.new_password.data = ''
		return render_template('user/change_password.html', title=title, form=form)

@app.route('/posts/<username>')
def get_user_posts(username):
		user = User.query.filter_by(username=username).first()
		return render_template(
			'post/user_posts.html', 
			posts=user.posts, 
			username=user.username
		)