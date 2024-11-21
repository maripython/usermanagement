from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except ConnectionError as ce:
    print(f"Unable to connect to MongoDB Server: {ce}")

db = client['UserManagement']

Users = db.users
