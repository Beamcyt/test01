from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

def easy_question():
    questions = [
        ("(2 + 2) เท่ากับเท่าไหร่?", 4),
        ("(10 - 3) เท่ากับเท่าไหร่?", 7),
        ("(5 * 4) เท่ากับเท่าไหร่?", 20),
        ("(8 / 2) เท่ากับเท่าไหร่?", 4),
        ("(9 + 6) เท่ากับเท่าไหร่?", 15),
        ("(1 + 1) เท่ากับเท่าไหร่?", 2),
        ("(7 + 2) เท่ากับเท่าไหร่?", 9),
        ("(4 + 4) เท่ากับเท่าไหร่?", 8),
        ("(3 + 2) เท่ากับเท่าไหร่?", 5),
        ("(10 + 6) เท่ากับเท่าไหร่?", 16),
         #เพิ่ม 10 ข้อ
        ("(23 + 45) เท่ากับเท่าไหร่?", 68),
        ("(63 + 29) เท่ากับเท่าไหร่?", 92),
        ("(56 + 43) เท่ากับเท่าไหร่?", 99),
        ("(56 + 78) เท่ากับเท่าไหร่?", 134),
        ("(105 - 48) เท่ากับเท่าไหร่?",57),
        ("(17 - 4) เท่ากับเท่าไหร่?", 13),
        ("(12 - 7) เท่ากับเท่าไหร่?", 5),
        ("(22 + 1) เท่ากับเท่าไหร่?", 23),
        ("(7 - 5) เท่ากับเท่าไหร่?", 2),
        ("(20 + 6) เท่ากับเท่าไหร่?", 26),
        #เพิ่ม 5 ข้อ
        ("(25 + 2) เท่ากับเท่าไหร่?", 27),
        ("(17 - 6) เท่ากับเท่าไหร่?", 11),
        ("(22 - 3) เท่ากับเท่าไหร่?", 19),
        ("(19 - 7) เท่ากับเท่าไหร่?", 12),
        ("(8 + 6) เท่ากับเท่าไหร่?", 14),
    ]
    return random.choice(questions)

def medium_question():
    questions = [
        ("(10 * 5) เท่ากับเท่าไหร่?", 50),
        ("(20 ÷ 4) เท่ากับเท่าไหร่?", 5),
        ("(15 + 8) เท่ากับเท่าไหร่?", 23),
        ("(18 - 7) เท่ากับเท่าไหร่?", 11),
        ("(25 * 4) เท่ากับเท่าไหร่?", 100),
        ("(42 ÷ 6) เท่ากับเท่าไหร่?", 7),
        ("(96 ÷ 8) เท่ากับเท่าไหร่?", 12),
        ("(16 + 19) เท่ากับเท่าไหร่?", 35),
        ("(7 * 2) เท่ากับเท่าไหร่?", 14),
        ("(8 * 3) เท่ากับเท่าไหร่?", 24),
        #เพิ่ม 10 ข้อ
        ("(11 * 4) เท่ากับเท่าไหร่?", 44),
        ("(3 * 12) เท่ากับเท่าไหร่?", 36),
        ("(7 * 9) เท่ากับเท่าไหร่?", 63),
        ("(36 ÷ 6) เท่ากับเท่าไหร่?", 6),
        ("(10 * 3) เท่ากับเท่าไหร่?",30),
        ("(3 * 7) เท่ากับเท่าไหร่?", 21),
        ("(15 ÷ 5) เท่ากับเท่าไหร่?", 3),
        ("(20 ÷ 10) เท่ากับเท่าไหร่?", 2),
        ("(16 ÷ 8) เท่ากับเท่าไหร่?", 2),
        ("(7 * 5) เท่ากับเท่าไหร่?",35),
        #เพิ่ม 5 ข้อ
        ("(4 * 8) เท่ากับเท่าไหร่?", 32),
        ("(9 * 4) เท่ากับเท่าไหร่?", 36),
        ("(12 ÷ 3) เท่ากับเท่าไหร่?", 4),
        ("(21 ÷ 7) เท่ากับเท่าไหร่?", 21),
        ("(16 ÷ 2) เท่ากับเท่าไหร่?", 8),
    ]
    return random.choice(questions)

def hard_question():
    questions = [
        ("(25 * 3) เท่ากับเท่าไหร่?", 75),
        ("(48 ÷ 8) เท่ากับเท่าไหร่?", 6),
        ("(11 * 7) เท่ากับเท่าไหร่?", 77),
        ("(63 ÷ 9) เท่ากับเท่าไหร่?", 7),
        ("(7 * 7) เท่ากับเท่าไหร่?", 49),
        ("(5 * 3) เท่ากับเท่าไหร่?", 15),
        ("(3 * 6) เท่ากับเท่าไหร่?", 18),
        ("(10 ÷ 2) เท่ากับเท่าไหร่?", 5),
        ("(80 ÷ 2) เท่ากับเท่าไหร่?", 40),
        ("(90 ÷ 3) เท่ากับเท่าไหร่?", 30),
        #เพิ่ม 10 ข้อ
        ("(543 + 876) เท่ากับเท่าไหร่?", 1419),
        ("(723 - 486) เท่ากับเท่าไหร่?", 237),
        ("(789 - 234) เท่ากับเท่าไหร่?", 555),
        ("(654 + 321) เท่ากับเท่าไหร่?", 975),
        ("(20 * 3) เท่ากับเท่าไหร่?",60), 
        ("(123 + 45) เท่ากับเท่าไหร่?", 168),
        ("(151 + 17) เท่ากับเท่าไหร่?", 168),
        ("(138 + 41) เท่ากับเท่าไหร่?", 179),
        ("(169 - 18) เท่ากับเท่าไหร่?", 151),
        ("(188 - 50) เท่ากับเท่าไหร่?",138),
        #เพิ่ม 5 ข้อ
        ("(220 ÷ 5) เท่ากับเท่าไหร่?", 44),
        ("(160 ÷ 4) เท่ากับเท่าไหร่?", 40),
        ("(144 ÷ 12) เท่ากับเท่าไหร่?",12),
        ("(57 * 3) เท่ากับเท่าไหร่?", 171),
        ("(68 * 9) เท่ากับเท่าไหร่?",612), 
    ]
    return random.choice(questions)

def get_question():
    global difficulty
    if difficulty == "easy":
        return easy_question()
    elif difficulty == "medium":
        return medium_question()
    elif difficulty == "hard":
        return hard_question()

def start_game():
    global score, difficulty, current_question, question_number
    score = 0
    difficulty = "medium"
    current_question = get_question()
    question_number = 1

start_game()

def check_game_completion():
    global score
    if score == 10:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    global score, current_question, difficulty, question_number
    if request.method == 'GET':
        if check_game_completion():
            return render_template('completion.html', score=score)
        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

    elif request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer = current_question[1]

        if user_answer == correct_answer:
            score += 1
            update_difficulty_on_correct()
        else:
            update_difficulty_on_incorrect()

        current_question = get_question()
        question_number += 1

        if question_number > 10:  # ตรวจสอบว่าทำข้อสอบครบ 10 ข้อหรือไม่
            return render_template('completion.html', score=score)

        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

@app.route('/start', methods=['POST'])
def start_new_game():
    start_game()
    return redirect('/')

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

if __name__ == '__main__':
    app.run(debug=True)