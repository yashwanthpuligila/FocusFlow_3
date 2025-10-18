# 📂 Where to Put Your MongoDB Code

## Quick Answer

You have **3 main options** for where to put MongoDB code:

---

## ✅ Option 1: Test Script (For Testing) - **RECOMMENDED FOR NOW**

**File:** `test_mongodb.py` (✅ Already created for you!)

**Location:** `Y:\Focus_Flow_3\FocusFlow\block_apps\test_mongodb.py`

**Use for:**
- Testing MongoDB connection
- Adding sample data
- Experimenting with queries
- Learning MongoDB operations

**Run it:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python test_mongodb.py
```

---

## ✅ Option 2: MongoDB Logger (For Production) - **RECOMMENDED**

**File:** `mongodb_logger.py` (✅ Already created for you!)

**Location:** `Y:\Focus_Flow_3\FocusFlow\block_apps\mongodb_logger.py`

**Use for:**
- Logging blocked apps
- Managing blocking rules
- Session tracking
- Getting statistics

**How to use in your existing blocker:**

### In `block_apps.py` or `AppBlocker.py`:

```python
from mongodb_logger import MongoDBLogger

# Initialize logger
logger = MongoDBLogger()

# Start a session
session_id = logger.log_session_start(duration_minutes=25, rules_count=5)

# Log when you block an app
logger.log_blocked_app('Chrome', 'chrome.exe')

# Get rules from database instead of file
rules = logger.get_blocking_rules()

# End session
logger.log_session_end(session_id, blocked_count=10)

# Get statistics
stats = logger.get_statistics()
print(f"Total blocked: {stats['total_blocked']}")
```

**Test it:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python mongodb_logger.py
```

---

## ✅ Option 3: Direct in Your Scripts

**Files:** Modify your existing files:
- `block_apps.py`
- `AppBlocker.py`
- Any custom script

**Example integration:**

```python
# At the top of block_apps.py
from mongo_helper import get_database
from datetime import datetime

# Add this function
def log_to_mongodb(app_name, process_name):
    db = get_database()
    if db is not None:
        db.blocked_apps_log.insert_one({
            'app_name': app_name,
            'process_name': process_name,
            'timestamp': datetime.now()
        })

# In your blocking loop, add:
def block_app(app_name):
    # ... your existing blocking code ...
    
    # Add MongoDB logging
    log_to_mongodb(app_name, process_name)
```

---

## 📁 Your Current File Structure

```
block_apps/
├── mongo_helper.py          ← ✅ MongoDB connection (already working)
├── test_mongodb.py          ← ✅ Test script (NEW - use this first!)
├── mongodb_logger.py        ← ✅ Logger class (NEW - use for production)
├── block_apps.py            ← Your main blocker
├── AppBlocker.py            ← Alternative blocker
├── app_blocklist.txt        ← Current blocklist file
└── block_enabled.txt        ← Enable/disable flag
```

---

## 🎯 Recommended Workflow

### Step 1: Test with `test_mongodb.py`

```powershell
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python test_mongodb.py
```

This will:
- Add test users
- Add blocking rules
- Show you how everything works

### Step 2: Test the Logger

```powershell
python mongodb_logger.py
```

This will:
- Test logging functionality
- Show statistics
- Demonstrate the API

### Step 3: Integrate with Your App Blocker

Choose ONE of these approaches:

**Approach A: Use the Logger Class (Recommended)**
```python
# In block_apps.py or AppBlocker.py
from mongodb_logger import MongoDBLogger

logger = MongoDBLogger()
session_id = logger.log_session_start(25, 5)
logger.log_blocked_app('Chrome', 'chrome.exe')
```

**Approach B: Direct MongoDB calls**
```python
# In block_apps.py or AppBlocker.py
from mongo_helper import get_database

db = get_database()
db.blocked_apps_log.insert_one({...})
```

---

## 💡 Quick Examples

### Example 1: Simple Test (Interactive Python)

```powershell
python
```

```python
>>> from mongo_helper import get_database
>>> db = get_database()
>>> db.users.insert_one({'username': 'john', 'email': 'john@test.com'})
>>> list(db.users.find())
>>> exit()
```

### Example 2: One-time Script

Create `Y:\Focus_Flow_3\FocusFlow\block_apps\my_test.py`:

```python
from mongo_helper import get_database

db = get_database()

# Add a user
db.users.insert_one({
    'username': 'test_user',
    'email': 'test@example.com'
})

# Query users
for user in db.users.find():
    print(user)
```

Run:
```powershell
python my_test.py
```

### Example 3: Integration (Production)

Modify `block_apps.py`:

```python
# Add at the top
from mongodb_logger import MongoDBLogger

# In main() function
logger = MongoDBLogger()
session_id = logger.log_session_start()

# In your blocking loop
for app in apps_to_block:
    # ... your blocking code ...
    logger.log_blocked_app(app, process_name)

# At the end
logger.log_session_end(session_id)
```

---

## 🚀 Quick Start Commands

```powershell
# Navigate to block_apps folder
cd Y:\Focus_Flow_3\FocusFlow\block_apps

# Test MongoDB connection
python mongo_helper.py

# Run test script (adds sample data)
python test_mongodb.py

# Test logger functionality
python mongodb_logger.py

# Interactive Python (for quick tests)
python
>>> from mongo_helper import get_database
>>> db = get_database()
>>> db.users.find_one()
```

---

## 📊 View Your Data

### Option 1: MongoDB Compass (GUI)
1. Download: https://www.mongodb.com/products/compass
2. Connect to: `mongodb+srv://yashwanthpuligila548:5485654@cluster1.p9g3qdo.mongodb.net/`
3. Browse database: `focusflow`

### Option 2: Python Script
```python
from mongo_helper import get_database

db = get_database()
print(f"Users: {db.users.count_documents({})}")
print(f"Rules: {db.rules.count_documents({})}")
print(f"Logs: {db.blocked_apps_log.count_documents({})}")
```

---

## ✅ Summary

**For Testing:**
- Use `test_mongodb.py` ← Start here!

**For Production:**
- Use `mongodb_logger.py` class in your existing scripts

**For Quick Experiments:**
- Create temporary `.py` files in the `block_apps/` folder
- Or use interactive Python shell

All MongoDB code goes in: `Y:\Focus_Flow_3\FocusFlow\block_apps\`

Start with `python test_mongodb.py` to see it in action! 🚀
