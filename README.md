# MusicLib

MusicLib is a web application developed using Flask that allows users to upload, listen and manage their music files. This README file provides information on how to set up the application, how to run it, and how to use its features.

## Setup

##### Clone The Repository

```bash
git clone https://github.com/kamalkish0r/music-app.git && cd music-app
```

#### System requirements

Python >= 3.8
Project built on Python 3.10.4

##### Create a virtual environment

On linux/mac

```bash
python3 -m venv env
```

##### Activate the virtual environment

```bash
source env/bin/activate
```

##### Install dependencies

```bash
pip3 install -r requirements.txt
```

##### Handling Secret Information

If you don't wish to use password reset then you can just add a fake email and 16 character password.

For `MAIL_PASSWORD` go to <a href="https://myaccount.google.com/u/5/security/" target="_blank">Google Account</a> this and enable 2-Step verification.
Generate `APP_PASSWORD` by clicking on App Password option just below the 2-Step Verification.
Paste this 16 character password when you are asked to enter `APP_PASSWORD` while running the following script.

You can follow <a href="https://stackoverflow.com/a/72734404/16777411/" target="_blank">these</a> steps for better explaination with pictures.

```bash
python3 setup_secrets.py
```

You can read more about this <a href="https://support.google.com/accounts/answer/185833?hl=en/" target="_blank">here</a>.

##### To create database tables

```bash
python manage.py create_db
```

##### To run the app

```bash
python3 run.py
```

The application can be accessed at `http://localhost:5000/` in a web browser.

## Features

#### MusicLib provides the following features:

-   User registration and login
-   Uploading music files (currently only mp3 files are supported)
-   Listening to music
-   Editing music file metadata (artist, title, album)
-   Searching for music files by title, artist or album
-   Deleting music files
-   Updating user profile information
-   Resetting passwords through email
