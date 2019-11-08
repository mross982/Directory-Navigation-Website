from app.email import send_email as se
from flask import render_template, current_app


def send_token_email(user):
	'''
	The interesting part in this function is that the text and HTML content for the emails 
	is generated from templates using the familiar render_template() function. The templates
	receive the user and the token as arguments, so that a personalized email message can be 
	generated.
	'''
	token = user.get_token()
	se.send_email('[Carease] set up your account',
			sender=app.config['ADMINS'][0],
			recipients=[user.email],
			text_body=render_template('email/send_token_email.txt',
			user=user, token=token),
			html_body=render_template('email/send_token_email.html',
			user=user, token=token))
