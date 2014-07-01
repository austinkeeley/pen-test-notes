import os
from flask import render_template
import markdown

from app import flask_app as app

current_dir = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def index():
    return render_template('index.html', selected='index')

@app.route('/about')
def about():
    return render_template('about.html', selected='about')

@app.route('/markdown/<template>')
def markdown_(template):
    print template
    with open('%s/markdown/%s.md' % (current_dir, template)) as md_file:
        md = ''.join(md_file.read())
        md = markdown.markdown(md)
        return render_template('md.html', md=md)
