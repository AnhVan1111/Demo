from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo ứng dụng Flask và SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vanpro123@localhost:5432/student_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mô hình bảng CLASS
class Class(db.Model):
    __tablename__ = 'CLASS'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(255), nullable=False)

# Mô hình bảng STUDENT
class Student(db.Model):
    __tablename__ = 'STUDENT'
    student_id = db.Column(db.String(255), primary_key=True)
    student_name = db.Column(db.String(255), nullable=False)

# Mô hình bảng SUBJECT
class Subject(db.Model):
    __tablename__ = 'SUBJECT'
    subject_id = db.Column(db.String(255), primary_key=True)
    subject_name = db.Column(db.String(255), nullable=False)

# Mô hình bảng ATTENDANCE_RECORD
class AttendanceRecord(db.Model):
    __tablename__ = 'ATTENDANCE_RECORD'
    attendance_record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(255), nullable=False)

# Hàm để thêm dữ liệu vào cơ sở dữ liệu
def insert_data():
    # Dữ liệu cho bảng CLASS
    classes = [
        {'class_id': 1, 'class_name': 'Class A'},
        {'class_id': 2, 'class_name': 'Class B'}
    ]

    # Dữ liệu cho bảng STUDENT
    students = [
        {'student_id': 'S001', 'student_name': 'John Doe'},
        {'student_id': 'S002', 'student_name': 'Jane Smith'}
    ]

    # Dữ liệu cho bảng SUBJECT
    subjects = [
        {'subject_id': 'SUB001', 'subject_name': 'Math'},
        {'subject_id': 'SUB002', 'subject_name': 'English'}
    ]

    # Dữ liệu cho bảng ATTENDANCE_RECORD
    attendance_records = [
        {'class_id': 1, 'subject_id': 'SUB001', 'student_id': 'S001', 'date': '2024-11-25 09:00:00', 'status': 'Present'},
        {'class_id': 1, 'subject_id': 'SUB002', 'student_id': 'S002', 'date': '2024-11-25 09:00:00', 'status': 'Absent'}
    ]

    # Thêm dữ liệu vào bảng CLASS
    for cls in classes:
        class_obj = Class(class_id=cls['class_id'], class_name=cls['class_name'])
        db.session.add(class_obj)

    # Thêm dữ liệu vào bảng STUDENT
    for student in students:
        student_obj = Student(student_id=student['student_id'], student_name=student['student_name'])
        db.session.add(student_obj)

    # Thêm dữ liệu vào bảng SUBJECT
    for subject in subjects:
        subject_obj = Subject(subject_id=subject['subject_id'], subject_name=subject['subject_name'])
        db.session.add(subject_obj)

    # Thêm dữ liệu vào bảng ATTENDANCE_RECORD
    for record in attendance_records:
        attendance_obj = AttendanceRecord(
            class_id=record['class_id'],
            subject_id=record['subject_id'],
            student_id=record['student_id'],
            date=datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S'),
            status=record['status']
        )
        db.session.add(attendance_obj)

    # Lưu các thay đổi vào cơ sở dữ liệu
    db.session.commit()

# Route để thêm dữ liệu vào cơ sở dữ liệu
@app.route('/add_data', methods=['POST', 'GET'])
def add_data():
    insert_data()
    return "Data inserted successfully!"

# Route để hiển thị danh sách lớp học
@app.route('/classes', methods=['POST', 'GET'])
def show_classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)

# Route để hiển thị danh sách sinh viên
@app.route('/students', methods=['POST', 'GET'])
def show_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

# Route để hiển thị danh sách môn học
@app.route('/subjects')
def show_subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

# Route để hiển thị bản ghi điểm danh
@app.route('/attendance')
def show_attendance():
    attendance_records = AttendanceRecord.query.all()
    return render_template('attendance.html', attendance_records=attendance_records)

# Route trang chủ
@app.route('/')
def index():
    return '''
        <h1>Welcome to the Attendance System</h1>
        <ul>
            <li><a href="/classes">Classes</a></li>
            <li><a href="/students">Students</a></li>
            <li><a href="/subjects">Subjects</a></li>
            <li><a href="/attendance">Attendance Records</a></li>
        </ul>
    '''

# Chạy ứng dụng Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo các bảng trong cơ sở dữ liệu nếu chưa tồn tại
    app.run(debug=True)
