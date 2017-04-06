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

@app.route("/<file_name>.txt")
def send_text_file(file_name):

    file_dot_text = file_name + ".txt"
    return app.send_static_file(file_dot_text)

'''
    expects a query string of the form
    ?
        PDB_IDS=<> a list of all the target PDB_IDS comman separated; if empty will assume all in databank
        keys=<> a list of all the target atoms in the isoalloxezene; if none, will assume all

'''
#""" Take the query string and render a CSV with all of the relevant fields. """
### @ Rahul this should be pretty easy:
###     open the data.csv in pandas and make some filters
###     if you're creative enough pandas has an SQL queiries feature
###     which might be useful; however, let me know if you need help
@app.route('/query', methods=['GET'])
def treat_query():

    '''
        expects a query string of the form
        ?
            PDB_IDS=<> a list of all the target PDB_IDS comman separated; if empty will assume all in databank
            keys=<> a list of all the target atoms in the isoalloxezene; if none, will assume all

    '''

    query_str = request.data
    # seperates the query string into the two criteria PDB_IDS and keys
    crit_list = query_str.split('\n')
    pdb_crit = crit_list[0]
    keys_crit = crit_list[1]

    # gets path for reading in csv
    folder_path = os.getcwd()
    data_path = os.path.join(folder_path, "data.csv")

    # gets path for writing the csv file later
    static_folder_path = os.path.join(folder_path, "static")
    file_out_path = os.path.join(static_folder_path, "output.csv")

    # gets csv file_name
    data_pd = pd.read_csv(data_path)

    # initializes variables to be used later
    pdb_ids_str = ""
    pdb_id_list = []

    keys_str = ""
    keys_list = []

    df_list = []

    if ((pdb_crit == "PDB_IDS=<>") and (keys_crit == "keys=<>")):
        print("tests")
        return app.send_static_file("data.csv")
    elif ((pdb_crit != "PDB_IDS=<>") and (keys_crit != "keys=<>")):

        # gets a list of the relevant pdb ids
        pdb_ids_str = pdb_crit[9:-1]
        pdb_id_list = pdb_ids_str.split(',')

        # gets a list of the relevant keys
        keys_str = keys_crit[6:-1]
        keys_list = keys_str.split(',')

        # gets all relevant rows based on pdb_id and key atoms
        for pdb_key in pdb_id_list:
            for key_id in keys_list:
                df_list.append(data_pd[(data_pd.target_atom_name == key_id) & (data_pd.PDB_ID == pdb_key)])

        # print(df_list)

        # combines all relevant dataframes into one
        df_final = pd.concat(df_list)

        # turns dataframe into csv file
        df_final.to_csv(path_or_buf=file_out_path)

        return None
    elif ((pdb_crit != "PDB_IDS=<>") and (keys_crit == "keys=<>")):

        # gets a list of the relevant pdb ids
        pdb_ids_str = pdb_crit[9:-1]
        pdb_id_list = pdb_ids_str.split(',')

        # makes a list of dataframes for rows that have relvant pdb_id
        for pdb_key in pdb_id_list:
            df_list.append(data_pd[data_pd.PDB_ID == pdb_key])

        # combines all relevant dataframes into one
        df_final = pd.concat(df_list)

        # turns dataframe to csv file
        df_final.to_csv(path_or_buf=file_out_path)

        return app.send_static_file("output.csv")
    else:

        # gets a list of the relevant keys
        keys_str = keys_crit[6:-1]
        keys_list = keys_str.split(',')

        # makes a list of dataframes from rows that have relevant keys
        for key_id in keys_list:
            df_list.append(data_pd[data_pd.target_atom_name == key_id])

        # appends all the dataframes to the first
        df_final = pd.concat(df_list)

        # turns dataframe to csv file
        df_final.to_csv(path_or_buf=file_out_path)

        return app.send_static_file("output.csv")
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
