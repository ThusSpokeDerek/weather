import env
import threading
import subprocess
import os
import sys
from flask import Flask, render_template, request, abort
from firebase import firebase

firebase = firebase.FirebaseApplication(env.db, None)

app = Flask(__name__)
app.debug = True

submit = False
# def run_script():
#     theproc = subprocess.Popen([sys.executable, "run_me.py"])
#     theproc.communicate()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', submit = False)

@app.route('/', methods=['POST', 'GET'])
def appForm():
    name = str(request.form['name'])
    cell = str(request.form['cell'])
    zipcode = str(request.form['zip'])
    time = str(request.form['time'])
    result = firebase.post('/client', {'name' : name, 'cell' : cell, 'zipcode' : zipcode, 'time' : time})
    if cell and zipcode:
    	return render_template('index.html', submit = True)
        
# @app.route('/generate')
# def generate():
#     # threading.Thread(target=lambda: run_script()).start()
#     return render_template('processing.html')
#
# @app.route('/is_done')
# def is_done():
#     hfile = "templates\\itworked.html"
#     if os.path.isfile(hfile):
#         return render_template('itworked.html')
#     else:
#         abort(404)

if __name__ == "__main__":
    app.run()
