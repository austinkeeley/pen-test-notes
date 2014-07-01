from flask import Flask, url_for

flask_app = Flask(__name__)


# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
flask_app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

from app import views
