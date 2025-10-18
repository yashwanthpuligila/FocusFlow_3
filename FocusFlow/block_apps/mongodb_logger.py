"""
MongoDB integration module for AppBlocker
This module adds database logging and rule management to the app blocker
"""

from mongo_helper import get_database
from datetime import datetime
import json
import time

class MongoDBLogger:
    """Logger for app blocking events to MongoDB"""
    
    def __init__(self):
        self.db = get_database()
    
    def log_blocked_app(self, app_name, process_name, action='blocked'):
        """Log when an app is blocked"""
        if self.db is not None:
            log_entry = {
                'app_name': app_name,
                'process_name': process_name,
                'action': action,
                'timestamp': datetime.now(),
                'status': 'success'
            }
            try:
                result = self.db.blocked_apps_log.insert_one(log_entry)
                print(f"📝 Logged to MongoDB: {app_name} {action} (ID: {result.inserted_id})")
                return result.inserted_id
            except Exception as e:
                print(f"❌ Failed to log to MongoDB: {e}")
                return None
        return None
    
    def log_session_start(self, duration_minutes=None, rules_count=0):
        """Log when a blocking session starts"""
        if self.db is not None:
            session = {
                'type': 'session_start',
                'start_time': datetime.now(),
                'duration_minutes': duration_minutes,
                'rules_count': rules_count,
                'status': 'active'
            }
            try:
                result = self.db.sessions.insert_one(session)
                print(f"🚀 Session started (ID: {result.inserted_id})")
                return result.inserted_id
            except Exception as e:
                print(f"❌ Failed to log session: {e}")
                return None
        return None
    
    def log_session_end(self, session_id, blocked_count=0):
        """Log when a blocking session ends"""
        if self.db is not None and session_id:
            try:
                self.db.sessions.update_one(
                    {'_id': session_id},
                    {
                        '$set': {
                            'end_time': datetime.now(),
                            'status': 'completed',
                            'apps_blocked_count': blocked_count
                        }
                    }
                )
                print(f"⏹️  Session ended (Blocked {blocked_count} apps)")
                return True
            except Exception as e:
                print(f"❌ Failed to update session: {e}")
                return False
        return False
    
    def get_blocking_rules(self):
        """Get blocking rules from MongoDB"""
        if self.db is not None:
            try:
                rules = list(self.db.rules.find({'type': 'BLACKLIST'}))
                targets = [rule['target'] for rule in rules]
                print(f"📋 Loaded {len(targets)} blocking rules from MongoDB")
                return targets
            except Exception as e:
                print(f"❌ Failed to load rules: {e}")
                return []
        return []
    
    def add_rule(self, app_name, target, rule_type='BLACKLIST'):
        """Add a new blocking rule to MongoDB"""
        if self.db is not None:
            rule = {
                'app_name': app_name,
                'target': target,
                'type': rule_type,
                'created_at': datetime.now()
            }
            try:
                result = self.db.rules.insert_one(rule)
                print(f"✅ Added rule: {app_name} → {target}")
                return result.inserted_id
            except Exception as e:
                print(f"❌ Failed to add rule: {e}")
                return None
        return None
    
    def get_statistics(self):
        """Get blocking statistics"""
        if self.db is not None:
            try:
                stats = {
                    'total_blocked': self.db.blocked_apps_log.count_documents({}),
                    'total_sessions': self.db.sessions.count_documents({}),
                    'total_rules': self.db.rules.count_documents({'type': 'BLACKLIST'}),
                    'active_sessions': self.db.sessions.count_documents({'status': 'active'})
                }
                return stats
            except Exception as e:
                print(f"❌ Failed to get statistics: {e}")
                return None
        return None
    
    def get_recent_blocks(self, limit=10):
        """Get recent blocked apps"""
        if self.db is not None:
            try:
                blocks = list(self.db.blocked_apps_log.find()
                             .sort('timestamp', -1)
                             .limit(limit))
                return blocks
            except Exception as e:
                print(f"❌ Failed to get recent blocks: {e}")
                return []
        return []

# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Logger Test")
    print("=" * 60)
    
    logger = MongoDBLogger()
    
    # Test logging
    print("\n1️⃣  Testing log_blocked_app...")
    logger.log_blocked_app('Chrome', 'chrome.exe')
    
    print("\n2️⃣  Testing session logging...")
    session_id = logger.log_session_start(duration_minutes=25, rules_count=5)
    time.sleep(1)  # Simulate some blocking activity
    logger.log_session_end(session_id, blocked_count=3)
    
    print("\n3️⃣  Testing get_blocking_rules...")
    rules = logger.get_blocking_rules()
    if rules:
        print(f"   Rules: {rules}")
    else:
        print("   No rules found. Adding sample rules...")
        logger.add_rule('Chrome', 'chrome.exe')
        logger.add_rule('YouTube', 'youtube.com')
        rules = logger.get_blocking_rules()
        print(f"   Rules after adding: {rules}")
    
    print("\n4️⃣  Getting statistics...")
    stats = logger.get_statistics()
    if stats:
        print(f"   📊 Statistics:")
        print(f"      Total Blocked: {stats['total_blocked']}")
        print(f"      Total Sessions: {stats['total_sessions']}")
        print(f"      Total Rules: {stats['total_rules']}")
        print(f"      Active Sessions: {stats['active_sessions']}")
    
    print("\n5️⃣  Getting recent blocks...")
    recent = logger.get_recent_blocks(limit=5)
    if recent:
        print(f"   📝 Recent blocks:")
        for block in recent:
            print(f"      - {block.get('app_name')} at {block.get('timestamp')}")
    
    print("\n" + "=" * 60)
    print("✅ MongoDB Logger test complete!")
    print("=" * 60)
