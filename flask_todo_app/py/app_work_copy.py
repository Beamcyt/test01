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

def A1_question():
    questions = [
        ("What is your name?", "My name is [insert name]."),
        ("How old are you?",  "I am [insert age] years old."),
        ("Where are you from?",  "I am from [insert country]."),
        ("What is this? (Pointing to an object)", "That is a [insert object]."),
        ("Can you spell 'cat'?",  "C-A-T"),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def A2_question():
    questions = [
        ("What do you like to do in your free time?", "I like to [insert activity]."),
        ("Describe your family.",  "My family has [insert number] members. We are [insert description, e.g., happy, big]."),
        ("What did you eat for breakfast today?",  "I had [insert food] for breakfast today."),
        ("How do you go to school/work?", "I go to school/work by [insert mode of transportation, e.g., bus, car]."),
        ("Can you tell the time?", "It is [insert time]."),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def B1_question():
    questions = [
        ("Describe your favorite hobby and why you enjoy it.", "My favorite hobby is [insert hobby]. I enjoy it because [insert reason]."),
        ("Talk about a memorable holiday you had.",  "One memorable holiday I had was when [insert details]."),
        ("Discuss your future plans.",  "In the future, I plan to [insert plans, e.g., study abroad, start a business]."),
        ("Describe your hometown.", "My hometown is [insert description, e.g., small, lively]. It is known for [insert notable features]."),
        ("Explain your opinion on technology.", "I think technology is [insert opinion, e.g., helpful, important] because [insert reason]."),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def B2_question():
    questions = [
        ("Discuss the advantages and disadvantages of living in a city.", "Living in a city has advantages such as [insert advantages] but also disadvantages like [insert disadvantages]."),
        ("Describe a book or movie you recently enjoyed and why.",  "I recently enjoyed [insert title]. It was [insert description] and I liked it because [insert reason]."),
        ("Discuss the importance of education in today's society.",  "Education is important because [insert reasons, e.g., it helps individuals succeed, it promotes social mobility]."),
        ("Talk about a challenging situation you faced and how you overcame it.", "One challenging situation I faced was [insert situation]. I overcame it by [insert actions taken]."),
        ("Explain your views on environmental conservation.", "I believe environmental conservation is important because [insert reasons, e.g., it protects natural habitats, it ensures a sustainable future]."),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def C1_question():
    questions = [
        ("Discuss the impact of globalization on culture.", "Globalization has influenced culture in various ways, such as [insert impacts, e.g., cultural exchange, homogenization]."),
        ("Analyze the role of social media in modern society.", "Social media plays a significant role in modern society by [insert roles, e.g., facilitating communication, shaping public opinion]."),
        ("Evaluate the effectiveness of renewable energy sources.", "Renewable energy sources are effective in [insert effectiveness, e.g., reducing carbon emissions, promoting sustainability] because [insert reasons]."),
        ("Discuss the ethical implications of genetic engineering.", "Genetic engineering raises ethical concerns such as [insert concerns, e.g., altering natural processes, potential misuse]."),
        ("Examine the challenges and opportunities of artificial intelligence.",  "Artificial intelligence presents challenges like [insert challenges, e.g., job displacement, privacy concerns] but also opportunities such as [insert opportunities, e.g., automation, medical advancements]."),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def C2_question():
    questions = [
        ("Critically analyze the role of government in ensuring economic stability.", "The government plays a crucial role in ensuring economic stability through [insert measures, e.g., fiscal policies, regulation of financial markets]."),
        ("Evaluate the impact of globalization on income inequality.",  "Globalization has contributed to income inequality by [insert impacts, e.g., widening the wealth gap, creating winners and losers in the global economy]."),
        ("Discuss the ethical considerations in conducting scientific research.", "Ethical considerations in scientific research include [insert considerations, e.g., informed consent, minimizing harm to subjects]."),
        ("Examine the role of international organizations in addressing global challenges.", "International organizations play a crucial role in addressing global challenges such as [insert challenges, e.g., climate change, poverty] by [insert actions, e.g., coordinating efforts, providing aid]."),
        ("Analyze the impact of digitalization on various sectors of society.",  "Digitalization has transformed various sectors of society, including [insert sectors, e.g., education, healthcare], by [insert impacts, e.g., increasing access to information, changing business models]."),
        # เพิ่มคำถาม...
    ]
    return random.choice(questions)

def collect_game_data():
    questions = []
    answers = []
    levels = []

    for _ in range(500):
        if random.random() < 0.4:
            question, answer = A1_question()
            levels.append('A1')
        elif random.random() < 0.7:
            question, answer = A2_question()
            levels.append('A2')
        else:
            question, answer = B1_question()
            levels.append('B1')
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
    difficulty = "A1"  # เริ่มต้นด้วยระดับความยากของเกมที่ประมาณกลาง
    current_question = get_question()  # เริ่มเกมด้วยคำถามระดับปานกลาง
    question_number = 1

start_game()

def get_question():
    global difficulty
    if difficulty == "easy":
        return A1_question()
    elif difficulty == "medium":
        return A2_question()
    elif difficulty == "hard":
        return B1_question()
    elif difficulty == "very_hard":
        return B2_question()
    elif difficulty == "expert":
        return C1_question()
    elif difficulty == "master":
        return C2_question()

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
            collect_game_data()  # เก็บข้อมูลเกมเมื่อเกมเสร็จสิ้น
            return render_template('completion.html', score=score)
        current_question = get_question()  # เรียกคำถามใหม่
        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

    elif request.method == 'POST':
        user_answer = request.form['answer']
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

        current_question = get_question()  # เรียกคำถามใหม่
        question_number += 1

        if question_number > 10:  # ตรวจสอบว่าทำข้อสอบครบ 10 ข้อหรือไม่
            collect_game_data()  # เก็บข้อมูลเกมเมื่อเกมเสร็จสิ้น
            return render_template('completion.html', score=score)

        return render_template('index.html', question=current_question[0], score=score, difficulty=difficulty, question_number=question_number)

# ฟังก์ชันใหม่สำหรับเก็บข้อมูลเกมลงใน Excel
def collect_game_data():
    df = pd.DataFrame(user_data)
    df.to_excel('static/user_game_data.xlsx', index=False)

@app.route('/start', methods=['POST'])
def start_new_game():
    start_game()
    return redirect('/')

def update_difficulty_on_correct():
    global difficulty
    if difficulty == "A1":
        difficulty = "A2"
    elif difficulty == "A2":
        difficulty = "B1"
    elif difficulty == "B1":
        difficulty = "B2"
    elif difficulty == "B2":
        difficulty = "C1"
    elif difficulty == "C1":
        difficulty = "C2"
    elif difficulty == "C2":
        pass

def update_difficulty_on_incorrect():
    global difficulty
    if difficulty == "A2":
        difficulty = "A1"
    elif difficulty == "B1":
        difficulty = "A2"
    elif difficulty == "B2":
        difficulty = "B1"
    elif difficulty == "C1":
        difficulty = "B2"
    elif difficulty == "C2":
        difficulty = "C1"
    elif difficulty == "A1":
        pass


if __name__ == "__main__":
    app.run(debug=True)
