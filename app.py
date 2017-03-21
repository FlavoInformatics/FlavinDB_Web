"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

"""
# To run the web app
import os
from flask import Flask, render_template, request, redirect, url_for

# to generate and use actual quieries
import pandas as pd
import numpy as np

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Main routes
###

@app.route('/', methods=['GET'])
def home():
    """Render website's home page."""
    return render_template('home.html')


'''
Example of how to send a text file

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
'''

'''
    expects a query string of the form
    ?
        PDB_IDS=<> a list of all the target PDB_IDS comman separated; if empty will assume all in databank
        keys=<> a list of all the target atoms in the isoalloxezene; if none, will assume all

'''
@app.route('/query', methods=['GET']):
    """ Take the query string and render a CSV with all of the relevant fields. """
    ### @ Rahul this should be pretty easy:
    ###     open the data.csv in pandas and make some filters
    ###     if you're creative enough pandas has an SQL queiries feature
    ###     which might be useful; however, let me know if you need help

    # incomplete
    return render_template('404.html'), 404

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response



###
# Various Error Handling
###


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
