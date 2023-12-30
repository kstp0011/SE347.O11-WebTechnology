from flask import url_for, current_app as app
from flask_mail import Message
from musicapp import mail


def send_password_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='MusicLib Password Reset Request',
                  recipients=[user.email], sender=app.config['MAIL_USERNAME'])
    msg.body = f'''To reset your password, please go to the following link :
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this mail.
Sincerely,
MusicLib
'''
    mail.send(msg)
