"""
Project Name: VidNotes
By: Donald Lee
Start date: Aug 14th 2021

Features:
Password protect?
Swap notes and video
History section? (Local storage)
make error text nicer
"""

from flask import Flask, render_template, url_for, redirect
import random, os, time
import smtplib, ssl
from email.message import EmailMessage

from datetime import date
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.background import BackgroundScheduler

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, RadioField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired, URL

import functions

# MongoDB
import dns # For mongodb to work, this installs an older version of bson, if version error, uninstall bson/pymongo to get it working again
import pymongo # If dnspython module error, do 'pip install pymongo[srv]'
MongoDBUsername = os.environ['MongoDBUsername']
MongoDBPassword = os.environ['MongoDBPassword']
client = pymongo.MongoClient("mongodb+srv://" + MongoDBUsername + ":" + MongoDBPassword + "@cluster0.aoruz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.database

# Checks database and deletes any expired collections
def deletes_expired():
    today = date.today()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    for note in db.notes.find():
        expiry_date = note['expiry_date']
        # If expired, delete
        if str(expiry_date) < str(today):
            db.notes.delete_one({"url_name":note['url_name']})

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

# Prevents cache from using the old css file, makes it use the updated one
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
# ^ ^ ^

# For CSRF, since it requires a secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class video_note_form(FlaskForm):
    video_link = StringField('Link', [validators.input_required(), validators.URL(require_tld=True, message="Invalid URL"), functions.is_youtube_video])
    title = StringField('Title')
    note  = TextAreaField('Note', [validators.input_required()], render_kw={"rows": 20, "cols": 50})
    autoplay = RadioField('autoplay', choices=[('yes_autoplay','Yes'),('no_autoplay','No')], validators=[InputRequired(message="You must select an option!")])
    email = StringField('email')

# Submits the video_note_form
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = video_note_form() 

    if form.validate_on_submit():
        video_link = form.video_link.data.strip(" ").replace('watch?v=', 'embed/')
        # Removes the extra URL text if the video is from a playlist
        video_link = video_link.split("&list=")[0]

        note = form.note.data.strip(" ")
        
        title = form.title.data.strip(" ")
        if len(title) == 0:
            title = "Untitled"

        autoplay = form.autoplay.data

        if autoplay == "yes_autoplay":
            # If the link doesn't have "?autoplay=1" in the link already, then add it
            if "?autoplay=1" not in video_link: 
                video_link = video_link + "?autoplay=1"
        # If note was duplicated, and former link had autoplay enabled
        else:
            video_link = video_link.replace('?autoplay=1', '') 
    

        url_name = functions.get_url_name()
        url_name_duplicate = True
        # Use a while loop to check to ensure that the url_name is not in the history database
        while url_name_duplicate == True:
            for data in db.url_names.find({"name":'url_names'}):
                used_names = data['url_names']

            if url_name in used_names:
                url_name = functions.get_url_name()
            else: # Not a duplicate, adds it to used name
                used_names.append(url_name)
                db.url_names.update_one({'name':'url_names'},{'$set':{'url_names':used_names}})
                url_name_duplicate = False

        expiry_date = str(date.today() + relativedelta(days=+21))
        # Don't need "autoplay" since it's within the video_link
        about_note = {
            "video_link": video_link,
            "title": title,
            "note": note,
            "url_name": url_name,
            "expiry_date": expiry_date
        }

        db.notes.insert_one(about_note)

        email = form.email.data.strip(" ")

        try:
            if email:
                gmail_user = os.environ['email']
                gmail_password = os.environ['password']

                subject = title
                body = f"{note}\n\nLink: https://vidnotes.donaldklee.repl.co/note/{url_name}\nLink expires after: {expiry_date}"

                msg = EmailMessage()
                msg.set_content(body)

                msg['Subject'] = subject
                msg['From'] = gmail_user
                msg['To'] = email

                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(msg['From'], gmail_password)
                server.send_message(msg)
                server.quit()
        except:
            print("Could not send email")

        return redirect(url_for('note', url_name = str(url_name)))

    return render_template("index.html", form=form)
    

@app.route('/')  # Home page
def home():
	return render_template("index.html", note_data=None, form=video_note_form())

class duplicate_note_form(FlaskForm):
    note_name = StringField('note_name', [validators.input_required()])

# Submits the video_note_form
@app.route('/duplicate', methods=['GET', 'POST'])
def duplicate():
    form = duplicate_note_form() 
    if form.validate_on_submit():
        note_name = form.note_name.data.strip(" ")

        for note in db.notes.find({'url_name': str(note_name)}):
            if len(note) > 0: # If that note has something
                foundnote = True

        if foundnote:
            print("FOUND NOTE\n\n")
            print(note)

            print("\n\n\n")

            return render_template("index.html", note_data=note, form=video_note_form())
    
    return render_template('404.html')
        

@app.route('/note/<url_name>')
def note(url_name):
    foundnote = False

    for note in db.notes.find({'url_name': str(url_name)}):
        if len(note) > 0: # If that note has something
            foundnote = True

    if foundnote:
        print(note)

        return render_template("note.html", note_data=note, form=duplicate_note_form())
    else:
        return render_template('404.html')

@app.route('/about')  # Home page
def about():
	return render_template("about.html")

@app.route('/faq')  # Home page
def faq():
	return render_template("faq.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Runs "deletes_expired" every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=deletes_expired, trigger="interval", seconds=300)
scheduler.start()

# For repl hosting
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True # Updates site when new changes are made
    )