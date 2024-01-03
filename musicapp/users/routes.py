from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from musicapp.models import User
from musicapp import bcrypt, db
from musicapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from musicapp.users.utils import send_password_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Successfully Created! Please login to continue.', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login Failed! Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('password_reset_request.html', title="Reset Password", form=form)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired!', 'warning')
        return redirect(url_for('users.password_reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! Please login to continue.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title="Reset Password", form=form)


@users.route('/admin')
@login_required
def admin():
    if not (current_user.is_admin):
        flash('You are not an admin!', 'danger')
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template('admin/admin.html', title='Admin', users=users)


@users.route('/admin/confirm_delete/<int:user_id>/<string:username>', methods=['POST'])
@login_required
def confirm_delete(user_id, username):
    if not (current_user.is_admin):
        flash('You are not an admin!', 'danger')
        return redirect(url_for('main.home'))

    return render_template('admin/confirm_delete.html', title='Confirm Delete', user_id=user_id, username=username)


@users.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    if not (current_user.is_admin):
        flash('You are not an admin!', 'danger')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    # only admin can delete user
    if user.is_admin or user.is_manager:
        flash('You cannot delete admin or manager!', 'danger')
        return redirect(url_for('users.admin'))

    user_username = user.username

    # delete the user from database
    db.session.delete(user)
    db.session.commit()

    flash(f'User `{user_username}` has been deleted!', 'success')
    return redirect(url_for('users.admin'))


@users.route('/admin/grant_manager/<int:user_id>', methods=['POST'])
@login_required
def grant_manager(user_id):
    if not (current_user.is_admin):
        flash('You are not an admin!', 'danger')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)

    user.is_manager = True
    db.session.commit()

    flash(f'User `{user.username}` has been granted manager!', 'success')
    return redirect(url_for('users.admin'))


@users.route('/admin/revoke_manager/<int:user_id>', methods=['POST'])
@login_required
def revoke_manager(user_id):
    if not (current_user.is_admin):
        flash('You are not an admin!', 'danger')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('You cannot revoke admin!', 'danger')
        return redirect(url_for('users.admin'))

    user.is_manager = False
    db.session.commit()

    flash(f'User `{user.username}` has been revoked manager!', 'success')
    return redirect(url_for('users.admin'))
