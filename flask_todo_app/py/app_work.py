from flask import Flask, render_template, request, redirect, send_file
import random
import pandas as pd
import os

app = Flask(__name__)

static_directory = os.path.join(app.root_path, 'static')
if not os.path.exists(static_directory):
    os.makedirs(static_directory)

user_answers = []

@app.route('/download_game_data')
def download_game_data():
    return send_file('static/game_data.xlsx', as_attachment=True)

def easy_question():
    questions = [
        ("(2 + 2) เท่ากับเท่าไหร่?", 4),
        ("(10 - 3) เท่ากับเท่าไหร่?", 7),
        # คำถามเพิ่มเติม...
    ]
    return random.choice(questions)

def medium_question():
    questions = [
        ("(10 * 5) เท่ากับเท่าไหร่?", 50),
        ("(20 ÷ 4) เท่ากับเท่าไหร่?", 5),
        # คำถามเพิ่มเติม...
    ]
    return random.choice(questions)

def hard_question():
    questions = [
        ("(25 * 8) เท่ากับเท่าไหร่?", 200),
        ("(12 * 9) เท่ากับเท่าไหร่?", 108),
        # คำถามเพิ่มเติม...
    ]
    return random.choice(questions)

def collect_game_data():
    questions = []
    answers = []
    levels = []

    for _ in range(500):
        if random.random() < 0.4:
            question, answer = easy_question()
            levels.append('ง่าย')
        elif random.random() < 0.7:
            question, answer = medium_question()
            levels.append('ปานกลาง')
        else:
            question, answer = hard_question()
            levels.append('ยาก')
        questions.append(question)
        answers.append(answer)

    df = pd.DataFrame({
        'คำถาม': questions,
        'คำตอบ': answers,
        'ระดับความยาก': levels
    })

    df.to_excel('static/game_data.xlsx', index=False)

def start_game():
    global score, difficulty, current_question, question_number
    score = 0
    difficulty = "medium"  # เริ่มต้นด้วยระดับความยากของเกมที่ประมาณกลาง
    current_question = medium_question()  # เริ่มเกมด้วยคำถามระดับปานกลาง
    question_number = 1

start_game()

def get_question():
    global difficulty
    if difficulty == "easy":
        return easy_question()
    elif difficulty == "medium":
        return medium_question()
    elif difficulty == "hard":
        return hard_question()

def check_game_completion():
    global score
    if score == 10:
        return True
    return False

# สร้าง list เพื่อเก็บข้อมูลของคำถามที่ผู้ใช้เจอและคำตอบที่ผู้ใช้ป้อน
user_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global score, current_question, difficulty, question_number, user_data
    if request.method == 'GET':
        if check_game_completion():
            collect_game_data(user_data)  # เก็บข้อมูลเกมเมื่อเกมเสร็จสิ้น
            return render_template('completion.html', score=score)
        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

    elif request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer = current_question[1]

        # เพิ่มข้อมูลของคำถามและคำตอบที่ผู้ใช้เจอลงใน list
        user_data.append({
            'คำถาม': current_question[0],
            'คำตอบที่ผู้ใช้ใส่': user_answer,
            'คำตอบที่ถูกต้อง': correct_answer,
            'คะแนน': score
        })

        if user_answer == correct_answer:
            score += 1
            update_difficulty_on_correct()
        else:
            update_difficulty_on_incorrect()

        current_question = get_question()
        question_number += 1

        if question_number > 10:  # ตรวจสอบว่าทำข้อสอบครบ 10 ข้อหรือไม่
            collect_game_data(user_data)  # เก็บข้อมูลเกมเมื่อเกมเสร็จสิ้น
            return render_template('completion.html', score=score)

        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

# ฟังก์ชันใหม่สำหรับเก็บข้อมูลเกมลงใน Excel
def collect_game_data(user_data):
    df = pd.DataFrame(user_data)
    df.to_excel('static/user_game_data.xlsx', index=False)
@app.route('/start', methods=['POST'])
def start_new_game():
    start_game()
    return redirect('/')

def update_user_answers(user_answer, correct_answer, question, score):
    user_answers.append({
        'Question': question,
        'User Answer': user_answer,
        'Correct Answer': correct_answer,
        'Score': score
    })

def update_difficulty_on_correct():
    global difficulty
    if difficulty == "hard":
        return
    elif difficulty == "medium":
        difficulty = "hard"
    elif difficulty == "easy":
        difficulty = "medium"

def update_difficulty_on_incorrect():
    global difficulty
    if difficulty == "hard":
        difficulty = "medium"
    elif difficulty == "medium":
        difficulty = "easy"
    elif difficulty == "easy":
        pass

if __name__ == "__main__":
    app.run(debug=True)
