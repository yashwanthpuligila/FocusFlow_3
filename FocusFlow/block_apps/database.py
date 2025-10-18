from mongo_helper import get_database

db = get_database()
db.users.insert_one({'username': 'test', 'email': 'test@example.com'})
for user in db.users.find():
    print(user)