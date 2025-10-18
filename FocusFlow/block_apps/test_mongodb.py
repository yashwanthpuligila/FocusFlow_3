"""
Test script for MongoDB operations
This file demonstrates how to use MongoDB with FocusFlow
"""

from mongo_helper import get_database
from datetime import datetime

def add_test_user():
    """Add a test user to the database"""
    db = get_database()
    
    if db is not None:
        # Add a user
        user = {
            'username': 'test_user',
            'email': 'test@example.com',
            'fullName': 'Test User',
            'createdAt': datetime.now(),
            'role': 'student'
        }
        
        result = db.users.insert_one(user)
        print(f"✅ User added with ID: {result.inserted_id}")
        return result.inserted_id
    else:
        print("❌ Failed to connect to database")
        return None

def query_all_users():
    """Query and display all users"""
    db = get_database()
    
    if db is not None:
        print("\n👥 All Users:")
        users = db.users.find()
        count = 0
        for user in users:
            count += 1
            print(f"  {count}. {user.get('username', 'N/A')} - {user.get('email', 'N/A')}")
            print(f"     ID: {user['_id']}")
        
        if count == 0:
            print("  No users found.")
        else:
            print(f"\n  Total: {count} users")
    else:
        print("❌ Failed to connect to database")

def add_sample_blocking_rules():
    """Add sample blocking rules"""
    db = get_database()
    
    if db is not None:
        rules = [
            {
                'app_name': 'Chrome',
                'type': 'BLACKLIST',
                'target': 'chrome.exe',
                'createdAt': datetime.now()
            },
            {
                'app_name': 'YouTube',
                'type': 'BLACKLIST',
                'target': 'youtube.com',
                'createdAt': datetime.now()
            },
            {
                'app_name': 'VS Code',
                'type': 'WHITELIST',
                'target': 'code.exe',
                'createdAt': datetime.now()
            }
        ]
        
        result = db.rules.insert_many(rules)
        print(f"✅ Added {len(result.inserted_ids)} blocking rules")
        return result.inserted_ids
    else:
        print("❌ Failed to connect to database")
        return None

def query_blocking_rules():
    """Query and display blocking rules"""
    db = get_database()
    
    if db is not None:
        print("\n🚫 Blocking Rules:")
        rules = db.rules.find()
        count = 0
        for rule in rules:
            count += 1
            rule_type = rule.get('type', 'N/A')
            emoji = '🚫' if rule_type == 'BLACKLIST' else '✅'
            print(f"  {emoji} {rule.get('app_name', 'N/A')} ({rule.get('target', 'N/A')}) - {rule_type}")
        
        if count == 0:
            print("  No rules found.")
        else:
            print(f"\n  Total: {count} rules")
    else:
        print("❌ Failed to connect to database")

def clear_all_data():
    """Clear all data from the database (use with caution!)"""
    db = get_database()
    
    if db is not None:
        response = input("\n⚠️  Are you sure you want to delete ALL data? (yes/no): ")
        if response.lower() == 'yes':
            db.users.delete_many({})
            db.rules.delete_many({})
            db.blocked_apps_log.delete_many({})
            print("✅ All data cleared!")
        else:
            print("❌ Cancelled")
    else:
        print("❌ Failed to connect to database")

if __name__ == "__main__":
    print("=" * 60)
    print("FocusFlow MongoDB Test Script")
    print("=" * 60)
    
    # Add test user
    print("\n1️⃣  Adding test user...")
    add_test_user()
    
    # Query all users
    print("\n2️⃣  Querying users...")
    query_all_users()
    
    # Add blocking rules
    print("\n3️⃣  Adding blocking rules...")
    add_sample_blocking_rules()
    
    # Query blocking rules
    print("\n4️⃣  Querying blocking rules...")
    query_blocking_rules()
    
    print("\n" + "=" * 60)
    print("✅ Test complete! Check MongoDB Compass to view your data.")
    print("=" * 60)
    
    # Uncomment to clear data
    # clear_all_data()
