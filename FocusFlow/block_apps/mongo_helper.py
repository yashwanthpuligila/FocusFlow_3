# block_apps/mongo_helper.py
import os
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Atlas connection
# IMPORTANT: Replace <db_password> with your actual password
# Better practice: Use environment variable
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '5485654')

# URL-encode the password (important for special characters like !)
encoded_password = quote_plus(MONGODB_PASSWORD)
uri = f"mongodb+srv://yashwanthpuligila548:{encoded_password}@cluster1.p9g3qdo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

def get_mongo_client():
    """
    Creates and returns a MongoDB client connection.
    Uses MongoDB Atlas with Server API v1.
    """
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        return client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

def get_database(db_name='focusflow'):
    """
    Returns the specified database.
    Default: focusflow
    """
    client = get_mongo_client()
    if client:
        return client[db_name]
    return None

def test_connection():
    """
    Tests the MongoDB connection and prints database info.
    """
    client = get_mongo_client()
    if client:
        try:
            # List all databases
            print("\n📊 Available databases:")
            for db in client.list_database_names():
                print(f"  - {db}")
            
            # Test focusflow database
            db = client['focusflow']
            print(f"\n📁 Collections in 'focusflow' database:")
            for collection in db.list_collection_names():
                count = db[collection].count_documents({})
                print(f"  - {collection}: {count} documents")
            
            client.close()
        except Exception as e:
            print(f"❌ Error testing connection: {e}")

# Usage in your blocking scripts
if __name__ == "__main__":
    print("🔌 Testing MongoDB Atlas connection...\n")
    test_connection()
    
    # Example: Query users
    print("\n👥 Fetching users...")
    db = get_database()
    if db is not None:
        users = db.users.find().limit(5)  # Limit to 5 users
        user_count = db.users.count_documents({})
        print(f"  Total users: {user_count}")
        for user in users:
            print(f"  - {user.get('username', 'N/A')} ({user.get('email', 'N/A')})")