from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import joblib
import os
#postgres://web_application_to_test_english_user:055KmoQ1l7OktjH0Idgg9Bw7l6UhkUKf@dpg-cokfkp779t8c73c9htbg-a.oregon-postgres.render.com/web_application_to_test_english
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  

MODEL_PATHS = [f'model_{i}.pkl' for i in range(1, 6)]
VECTORIZER_PATHS = [f'vectorizer_{i}.pkl' for i in range(1, 6)]

models = []
vectorizers = []
for model_path, vectorizer_path in zip(MODEL_PATHS, VECTORIZER_PATHS):
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        models.append(model)
        vectorizers.append(vectorizer)
    except Exception as e:
        print(f"Error loading model or vectorizer {model_path}/{vectorizer_path}: {e}")
        models.append(None)
        vectorizers.append(None)

def get_question():
    return [
        {"text": "Question 1: Describe the picture shown.", "images": ["image/1.jpg"]},
        {"text": "Question 2: Describe the picture shown.", "images": ["image/2.jpg"]},
        {"text": "Question 3: Describe the picture shown.", "images": ["image/3.jpg"]},
        {"text": "Question 4: Describe the picture shown.", "images": ["image/4.jpg"]},
        {"text": "Question 5: Describe the picture shown.", "images": ["image/5.jpg"]},
    ]

def save_to_excel(user_id, question, answer):
    filename = 'user_responses.xlsx'
    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['ID', 'Question', 'Answer'])
    new_row = pd.DataFrame({'ID': [user_id], 'Question': [question], 'Answer': [answer]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(filename, index=False)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_id'] = request.form.get('user_id')
        if session.get('user_id'):
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    questions = get_question()
    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    current_index = session['current_question_index']

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        session['user_answer'] = user_answer  
        question_text = questions[current_index]['text']

        save_to_excel(session['user_id'], question_text, user_answer)

        if current_index >= 4:
            session.pop('current_question_index', None)
            return redirect(url_for('completion'))
        else:
            session['current_question_index'] = current_index + 1
        return redirect(url_for('index'))

    current_question = questions[current_index]
    return render_template('index.html', question=current_question, question_number=current_index+1)


@app.route('/completion', methods=['GET'])
def completion():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        df = pd.read_excel('user_responses.xlsx')
    except Exception as e:
        return f"<p>Error reading Excel file: {e}</p>"

    if 'Answer' not in df.columns:
        return "<p>Column 'Answer' not found in Excel file.</p>"

    df['Answer'] = df['Answer'].replace(np.nan, '', regex=True)

    predictions = {}
    for i, (model, vectorizer) in enumerate(zip(models, vectorizers)):
        question_answers = df[df['Question'] == f'Question {i+1}']['Answer']
        question_predictions = []
        for answer in question_answers:
            if answer and model and vectorizer:
                transformed_input = vectorizer.transform([answer])
                prediction = model.predict(transformed_input)
                question_predictions.append(prediction[0])
            else:
                question_predictions.append("No answer")
        predictions[f"Question {i+1}"] = question_predictions

    return render_template('completion.html', predictions=predictions)


if __name__ == '__main__':
    app.run(debug=True)
