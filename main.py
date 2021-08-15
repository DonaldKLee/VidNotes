"""
Project Name: Leadeo
By: Donald Lee
Start date: Aug 14th 2021


Show a preview of the youtube video
Add to mongodb database along side a very long generated code
Ensure that it is not reused
When go to that link, show video etc

"""

from flask import Flask, render_template
import random, os

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, RadioField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired

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
    video_link = StringField('Link', validators=[validators.input_required()])
    note  = TextAreaField('Note', validators=[validators.input_required()], render_kw={"rows": 20, "cols": 50})
    autoplay = RadioField('', choices=[('yes_autoplay','Yes'),('no_autoplay','No')], validators=[InputRequired()])

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = video_note_form() 
    video_link = form.video_link.data.strip(" ")
    note = form.note.data.strip(" ")
    autoplay = form.autoplay.data

    print(video_link)
    print(note)
    print(autoplay)
    
    return render_template("index.html", form=video_note_form())


@app.route('/')  # '/' for the default page
def home():
	return render_template("index.html", form=video_note_form())


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True # Updates site when new changes are made
    )