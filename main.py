"""
Project Name: Leadeo
By: Donald Lee
Start date: Aug 14th 2021


Add to mongodb database along side a very long generated code
Ensure that it is not reused
When go to that link, show video etc

"""

from flask import Flask, render_template, url_for
import random, os

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, RadioField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired, URL

import functions

# MongoDB
import pymongo # If dnspython module error, do 'pip install pymongo[srv]'
MongoDBUsername = os.environ['MongoDBUsername']
MongoDBPassword = os.environ['MongoDBPassword']
client = pymongo.MongoClient("mongodb+srv://" + MongoDBUsername + ":" + MongoDBPassword + "@cluster0.aoruz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.database



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
    video_link = StringField('Link', [validators.input_required(), validators.URL(require_tld=True, message="Invalid URL")])
    note  = TextAreaField('Note', [validators.input_required()], render_kw={"rows": 20, "cols": 50})
    autoplay = RadioField('autoplay', choices=[('yes_autoplay','Yes'),('no_autoplay','No')], validators=[InputRequired(message="You must select an option!")])

# Submits the video_note_form
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = video_note_form() 
    if form.validate_on_submit():
        video_link = form.video_link.data.strip(" ").replace('watch?v=', 'embed/')
        note = form.note.data.strip(" ")
        
        autoplay = form.autoplay.data
        if autoplay == "yes_autoplay":
            video_link = video_link + "?autoplay=1"

        url_name = functions.get_url_name()

        # Use a while loop to check to ensure that the url_name is not in the history database


        # Don't need "autoplay" since it's within the video_link
        about_note = {
            "video_link": video_link,
            "note": note,
            "url_name": url_name
        }


        return render_template("index.html", form=form)
    return render_template("index.html", form=form)
    

@app.route('/')  # Home page
def home():
	return render_template("index.html", form=video_note_form())


# For repl hosting
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True # Updates site when new changes are made
    )