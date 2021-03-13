"import the required libraries"
from concurrent import futures
from flask import Flask, redirect, request, render_template
from utils.helper import Predictions
import os
#from concurrent.futures import ThreadPoolExecutor
import threading

#app
app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
#set the email
pred = ['Reccomendations are not yet ready! Refresh the page after 2 minutes!']
def thread_function(mlist, rlist, email):
    global pred
    print('Executing Thread')
    pred = Predictions.check_user(mlist, rlist, email)
    print('Finished Thread')

# home route
@app.route('/', methods = ['GET', 'POST'])
def set_model():
    '''
    Function to render the homepage and
    set the ml parameters.
    '''
    #get the movie titles
    titles = Predictions.get_titles()
    if request.method == "POST":
        req = request.form
        email = req.get('email')
        mlist = req.getlist('movies[]')
        rlist = req.getlist('ratings[]')
        #call the function to set the ml paramteres
        threading.Thread(target=thread_function, args=(mlist, rlist, email)).start()
        return redirect("/rec")


    return render_template("home.html", titles=titles)

#recommendations
@app.route('/rec', methods = ['GET'])
def show_rec():
    return render_template("recommendations.html", recommendation = pred)

if __name__ == "__main__":
    app.run(debug=True)

