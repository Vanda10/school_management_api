from pymongo.mongo_client import MongoClient

url = "mongodb+srv://vandabest123:cIdi3dW0H0XX3ybH@wctproject.eijrruy.mongodb.net/"
client = MongoClient(url)

db = client.school_management
student_db = db.student
teacher_db = db.teacher
course_db = db.departcourse
classes_db = db.classes
schedule_db = db.class_schedule
admin_db = db.admin
department_db = db.department
teacherCourse_db = db.teacher_course