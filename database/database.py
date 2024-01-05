from pymongo.mongo_client import MongoClient

url = "mongodb+srv://vandabest123:cIdi3dW0H0XX3ybH@wctproject.eijrruy.mongodb.net/"
client = MongoClient(url)

db = client.school_management
student_db = db.student
teacher_db = db.teacher
course_db = db.course
classes_db = db.classes
schedule_db = db.class_schedule