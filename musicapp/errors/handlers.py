from flask import Blueprint, render_template, redirect, request, flash

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/404.html'), 500


@errors.app_errorhandler(413)
def error_413(error):
    flash("File SIZE LIMIT EXCEEDED! Only files of size less than 20MB are allowed.", 'danger')
    return redirect(request.url)
