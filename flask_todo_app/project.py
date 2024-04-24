import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from joblib import dump

# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv('DataEnglishQ1 - ชีต1.csv')

# สร้าง mapping ของค่า 'Rank' เป็นตัวเลข
rank_mapping = {'A1': 0, 'A2': 1, 'B1': 2, 'B2': 3, 'C1': 4, 'C2': 5}

# แปลงค่า 'Rank' เป็นตัวเลขโดยใช้ mapping
df['Rank'] = df['Rank'].map(rank_mapping)

# แบ่งข้อมูลเป็น train และ test sets
X_train, X_test, y_train, y_test = train_test_split(df['Answer'], df['Rank'], test_size=0.2, random_state=42)

# สร้าง CountVectorizer เพื่อแปลงข้อความให้กลายเป็น feature vectors
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# สร้างโมเดล SVM
svm_model = SVC()
svm_model.fit(X_train_vec, y_train)

# ใช้โมเดล SVM ที่ train ได้ทำนายค่า target ของข้อมูลทดสอบ
y_pred_svm = svm_model.predict(X_test_vec)

# สร้าง Classification Report สำหรับ SVM
report_svm = classification_report(y_test, y_pred_svm)

# แสดงผลลัพธ์ของ Classification Report สำหรับ SVM
print("Classification Report for SVM:\n", report_svm)

# บันทึกโมเดล SVM ไปยังไฟล์ชื่อ svm_model.joblib
dump(svm_model, 'svm_model.joblib')
