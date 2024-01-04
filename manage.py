from flask.cli import FlaskGroup
from musicapp import create_app, db
import os
from musicapp.config import Config
from musicapp.models import User, Song, Artist_info, Like, Comment, Reply

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Create database tables."""
    db.create_all()


@cli.command("drop_db")
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    # delete all files in upload folder
    folder = Config.UPLOAD_FOLDER
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        os.remove(file_path)
    folder = Config.UPLOAD_FOLDER_IMAGES
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if filename != 'default.png':
            os.remove(file_path)


@cli.command("create_admin")
def create_admin():
    """Create admin user."""
    from musicapp.models import User
    from musicapp import bcrypt
    import pwinput

    username = input("Enter username: ")
    email = input("Enter email: ")
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        print("Admin user already exists.")
        return

    password = ''
    reinput_password = ' '

    while password != reinput_password:
        password = pwinput.pwinput(prompt='Enter password: ')
        if len(password) < 6:
            print("Password must be at least 6 characters long. Please try again.")
            continue
        reinput_password = pwinput.pwinput(prompt='Re-enter password: ')
        if password != reinput_password:
            print("Passwords do not match. Please try again.")

    password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(username=username,
                email=email, password=password, is_admin=True, is_manager=True)

    db.session.add(user)
    db.session.commit()


@cli.command("clear_db")
def clear_db():
    # clear data from all tables but keep the schema

    User.query.delete()
    Song.query.delete()
    Artist_info.query.delete()
    Like.query.delete()
    Comment.query.delete()
    Reply.query.delete()

    db.session.commit()
    # drop all files in upload folder
    import os
    from musicapp.config import Config
    folder = Config.UPLOAD_FOLDER
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        os.remove(file_path)
    folder = Config.UPLOAD_FOLDER_IMAGES
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if filename != 'default.png':
            os.remove(file_path)


if __name__ == "__main__":
    cli()
