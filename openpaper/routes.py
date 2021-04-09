from flask import render_template, flash, redirect, url_for, request
from openpaper import app, db
from openpaper.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from openpaper.models import User, Post
from werkzeug.urls import url_parse


@app.route('/')
def home():
    return(render_template('main.html'))


# @app.route('/read/')
# def read():
#     return(render_template('read.html'))

@app.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, abstract=form.abstract.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Submitted!')
        return redirect(url_for('home'))
    return(render_template('stream/submit.html', title='Submit', form=form))


@app.route('/papers')
def papers():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('stream/index.html', posts=posts)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)
