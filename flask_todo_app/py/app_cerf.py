from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_question():
    return [
        {"text": "Question 1: Introduce yourself", "images": ["image/1.jpg"]},
        {"text": "Question 2: What is your favorite programming language?", "images": ["image/2.jpg"]},
        {"text": "Question 3: Introduce yourself", "images": ["image/3.jpg"]},
        {"text": "Question 4: Introduce yourself", "images": ["image/4.jpg"]},
        {"text": "Question 5: Introduce yourself", "images": ["image/5.jpg"]},
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
     # เปลี่ยนเส้นทางไปยังหน้า login โดยไม่ต้องตรวจสอบสถานะการเข้าสู่ระบบ
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_id'] = request.form.get('user_id')
        # ตรวจสอบว่ามีการตั้งค่า user_id ใน session
        if session.get('user_id'):
            return redirect(url_for('before_exam'))  # เปลี่ยนเส้นทางไปยังหน้า index ถ้าเข้าสู่ระบบแล้ว
    # แสดงหน้า login ถ้ายังไม่เข้าสู่ระบบหรือเป็นการเข้าถึงด้วยวิธี GET
    return render_template('login.html')

@app.route('/before_exam')
def before_exam():
    # ตรวจสอบว่าผู้ใช้เข้าสู่ระบบหรือไม่
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('Before_exam.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    questions = get_question()
    # ตั้งค่าดัชนีคำถามเริ่มต้นหากไม่มีการตั้งค่าใน session
    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    current_index = session['current_question_index']

    if request.method == 'POST':
        user_id = session['user_id']
        user_answer = request.form.get('answer')
        question_text = questions[current_index]['text']

        save_to_excel(user_id, question_text, user_answer)

        # ตรวจสอบว่าถึงคำถามที่ 5 หรือไม่
        if current_index >= 4:
            # คำถามถึง 5 ข้อแล้ว, ล้างข้อมูล session และเปลี่ยนเส้นทางไปยังหน้า completion
            session.pop('current_question_index', None)
            return redirect(url_for('completion'))
        else:
            # ยังไม่ถึง 5 ข้อ, อัปเดตดัชนีสำหรับคำถามถัดไป
            session['current_question_index'] = current_index + 1
        return redirect(url_for('index'))

    # แสดงคำถามปัจจุบันถ้าไม่ใช่ POST request หรือยังมีคำถาม
    current_question = questions[current_index]
    return render_template('index.html', question=current_question, question_number=current_index+1)


@app.route('/completion', methods=['GET'])
def completion():
    # ตรวจสอบสถานะการเข้าสู่ระบบ
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('completion.html')

if __name__ == '__main__':
    app.run(debug=True)
