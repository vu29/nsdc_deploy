from flask import Flask,render_template,request


app = Flask(__name__)


# -- routes --

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pre_training', methods = ['GET','POST'] )
def pre_training():
    if request.method == 'POST':
        return request.form
        return render_template('pre_training.html')

    return render_template('pre_training.html')

@app.route('/post_training', methods = ['GET','POST'] )
def post_training():
    if request.method == 'POST':
        return render_template('post_training.html')
        
    return render_template('post_training.html')


if __name__ == "__main__":
    app.run(debug=True)