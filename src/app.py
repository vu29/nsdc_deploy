from flask import Flask,render_template,request
import json

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
        return request.form
        return render_template('post_training.html')

    dic = {
    "Gender" : {
        "Male" : 1,
        "Female" : 2
    },
    "Type of Disability": {"None": 1,
        "Deaf": 2,
        "Locomotor Disability": 3,
        "Low-vision": 4,
        "Blindness (Visually Impaired)": 6,
        "Leprosy Cured Person": 7,
        "Hard of Hearing": 8,
        "Speech and Language Disability (Speech Impaired)": 9,
        "Mental Behavior- Mental Illness, Mental Retardation": 10,
        "Cerebral Palsy": 11,
        "Muscular Dystrophy": 12,
        "Dwarfism": 13
    },
    "castecategory": {"Gen": 1,
    "SC": 2,
    "OBC": 3,
    "ST": 4
    }
}

    


    return render_template('post_training.html',category = dic)


if __name__ == "__main__":
    app.run(debug=True)