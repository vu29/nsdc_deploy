import json
import string
import random
from flask import Flask, render_template, request
from flask.globals import session
from pandas.core.arrays import categorical
from pandas.core.indexes import category
from utils import *

app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# select values
pre_train_select = json.load(
    open('./static/json/pre_training_select_val.json', 'r'))
post_train_select = json.load(
    open('./static/json/post_training_select_val.json', 'r'))


# Routes
@app.route('/')
def home():
    return render_template('home.html', title="Home")


@app.route('/pre_training', methods=['GET', 'POST'])
def pre_training():
    if request.method == 'POST':
        data = get_prediction_without_result(request.form)
        return render_template('result.html',title = 'Result',data = data)

    return render_template('pre_training.html', title="Pre-Training", category=pre_train_select)


@app.route('/post_training', methods=['GET', 'POST'])
def post_training():
    if request.method == 'POST':
        data = get_prediction_with_result(request.form)
        return render_template('result.html',title = 'Result', data = data)

    return render_template('post_training.html', title="Post-Training", category=post_train_select)


@app.route('/predict/user_info', methods=['GET','POST'])
def predict_user_info():
    if request.method == 'POST':
        return request.form
    
    return render_template('predict_1.html',title = 'Predict',category = post_train_select)

@app.route('/predict/tc_name', methods = ['POST'])
def tc_name():
    dist_code = request.form['TC District']
    session['user_info'] = request.form.to_dict()
    print(session)
    category = dict()
    category['TC Name'] = get_tc(dist_code)
    return render_template('predict_2.html',title = 'Predict',category = category, next_url = '/predict/partner_name')

@app.route('/predict/partner_name', methods = ['POST'])
def parter_name():
    session['TC Name'] = request.form['TC Name']
    print(session)
    category = dict()
    category['Partner Name'] = get_partner(session['user_info']['TC District'],session['TC Name'])
    return render_template('predict_2.html',title = 'Predict',category = category, next_url = '/predict/sector_name')

@app.route('/predict/sector_name', methods = ['POST'])
def sector_name():
    session['PartnerName'] = request.form['Partner Name']
    print(session)
    category = dict()
    category['Sector Name'] = get_sector(session['user_info']['TC District'],session['TC Name'],session['PartnerName'])
    return render_template('predict_2.html',title = 'Predict',category = category, next_url = '/predict/job_role')
    
@app.route('/predict/job_role', methods = ['POST'])
def job_role():
    session['SectorName'] = request.form['Sector Name']
    print(session)
    category = dict()
    category['Job Role'] = get_job_role(session['user_info']['TC District'],session['TC Name'],session['PartnerName'],session['SectorName'])
    return render_template('predict_2.html',title = 'Predict',category = category, next_url = '/predict/result')

@app.route('/predict/result', methods = ['POST'])
def predict_result():
    final_dict = {}
    for key in dict(session).keys():
        if(key == 'user_info'):
            final_dict.update(session[key])
        else:
            final_dict[key] = session[key]
    final_dict.update(request.form)
    print(final_dict)
    return str(get_prediction(final_dict))

if __name__ == "__main__":
    app.run(debug=True)
