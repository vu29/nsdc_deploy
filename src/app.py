import json
import requests
from flask import Flask, render_template, request



app = Flask(__name__)

# select values
pre_train_select = json.load(open('./static/json/pre_training_select_val.json','r'))
post_train_select = json.load(open('./static/json/post_training_select_val.json','r'))


# Routes
@app.route('/')
def home():
    return render_template('home.html', title = "Home")


@app.route('/pre_training', methods=['GET', 'POST'])
def pre_training():
    if request.method == 'POST':
        return render_template('result.html',title = 'Result')

    return render_template('pre_training.html',title="Pre-Training", category=pre_train_select)


@app.route('/post_training', methods=['GET', 'POST'])
def post_training():
    if request.method == 'POST':
        return request.form

    return render_template('post_training.html', title="Post-Training" ,category=post_train_select)


if __name__ == "__main__":
    app.run(debug=True)
