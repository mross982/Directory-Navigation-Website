from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        if user:
        	db.session.add(user)
	        db.session.commit()
	        # send_token_email(user)
        	flash('Congratulations, you have added a new registered user!')
        form = RegistrationForm()
        return redirect(url_for('register.html', title='Register', form=form))
    return render_template('register.html', title='Register', form=form)


# @bp.route('/set_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     '''
# 	Used by admin to  create a new user and send that user a token with which he/she will create a password
# 	and be logged in. 
#     '''
#     # form = SetPasswordRequestForm()
#     form = CreateUserForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         send_token_email(user)
#         flash('Check your email for the instructions to reset your password')
#         return redirect(url_for('login'))
#     return render_template('reset_password_request.html',
#                            title='Reset Password', form=form)


# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated: #Make sure user isn't logged in
#         return redirect(url_for('index'))
#     user = User.verify_reset_password_token(token) # verify token returning user
#     if not user:
#         return redirect(url_for('index')) # if the token was not verified, returned None
#     form = SetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('login'))
#     return render_template('reset_password.html', form=form)