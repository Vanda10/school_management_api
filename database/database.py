from pymongo.mongo_client import MongoClient

url = "mongodb+srv://vandabest123:cIdi3dW0H0XX3ybH@wctproject.eijrruy.mongodb.net/"
client = MongoClient(url)

db = client.school_management
student_db = db.student
teacher_db = db.teacher