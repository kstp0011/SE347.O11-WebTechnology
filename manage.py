from flask.cli import FlaskGroup
from musicapp import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Create database tables."""
    db.create_all()


if __name__ == "__main__":
    cli()
