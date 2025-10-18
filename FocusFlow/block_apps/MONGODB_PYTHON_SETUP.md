# MongoDB Atlas Setup for Python Scripts

## 🔐 Security Setup (IMPORTANT!)

### Option 1: Use Environment Variable (Recommended)

**Step 1:** Create a `.env` file in the `block_apps` folder:

```bash
# block_apps/.env
MONGODB_PASSWORD=YourActualPassword123!
```

**Step 2:** Install python-dotenv:
```powershell
pip install python-dotenv
```

**Step 3:** Update `mongo_helper.py` to load .env:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top
```

**Step 4:** Add `.env` to `.gitignore`:
```
# In your .gitignore file
block_apps/.env
*.env
```

### Option 2: Replace Password Directly (Not Recommended)

Open `mongo_helper.py` and replace `<db_password>` with your actual password:

```python
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'YourActualPassword123!')
```

---

## 🧪 Test Your Connection

Run the test script:

```powershell
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python mongo_helper.py
```

**Expected Output:**
```
🔌 Testing MongoDB Atlas connection...

✅ Successfully connected to MongoDB Atlas!

📊 Available databases:
  - admin
  - focusflow
  - local

📁 Collections in 'focusflow' database:
  - users: 5 documents
  - rules: 10 documents

👥 Fetching users...
  - john_doe (john@example.com)
  - jane_smith (jane@example.com)
```

---

## 🔧 Using MongoDB in Your Scripts

### Example 1: Query Users
```python
from mongo_helper import get_database

db = get_database()
users = db.users.find({'email': 'user@example.com'})
for user in users:
    print(user)
```

### Example 2: Get Blocking Rules
```python
from mongo_helper import get_database

db = get_database()
rules = db.rules.find({'type': 'BLACKLIST'})
for rule in rules:
    print(f"Block: {rule['target']}")
```

### Example 3: Insert Data
```python
from mongo_helper import get_database

db = get_database()
result = db.blocked_apps.insert_one({
    'app_name': 'Chrome',
    'blocked_at': '2025-10-18',
    'reason': 'Focus session'
})
print(f"Inserted ID: {result.inserted_id}")
```

---

## 📝 Connection String Breakdown

Your connection string:
```
mongodb+srv://yashwanthpuligila548:<db_password>@cluster1.p9g3qdo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1
```

- **Protocol:** `mongodb+srv://` (Atlas cloud)
- **Username:** `yashwanthpuligila548`
- **Password:** `<db_password>` (needs to be replaced)
- **Cluster:** `cluster1.p9g3qdo.mongodb.net`
- **Options:** 
  - `retryWrites=true` - Auto retry failed writes
  - `w=majority` - Write concern
  - `appName=Cluster1` - Application identifier

---

## 🛡️ Security Best Practices

1. ✅ **Never commit passwords** to Git
2. ✅ **Use environment variables** for sensitive data
3. ✅ **Restrict MongoDB Atlas IP whitelist** to your IP only
4. ✅ **Use strong passwords** (letters, numbers, symbols)
5. ✅ **Create separate users** for different applications
6. ✅ **Use least privilege** - only grant needed permissions

---

## 🔍 MongoDB Atlas Dashboard

1. Login to: https://cloud.mongodb.com
2. Navigate to your cluster: **Cluster1**
3. Check:
   - ✅ IP Whitelist (Network Access)
   - ✅ Database Users
   - ✅ Connection strings

---

## 🐛 Troubleshooting

### Error: Authentication failed
```
❌ MongoDB connection failed: Authentication failed
```
**Solution:** Check your password is correct and URL-encoded if it contains special characters.

### Error: IP not whitelisted
```
❌ MongoDB connection failed: connection timeout
```
**Solution:** Add your IP address in MongoDB Atlas → Network Access → Add IP Address

### Error: DNS resolution failed
```
❌ MongoDB connection failed: DNS name not found
```
**Solution:** Ensure `pymongo[srv]` and `dnspython` are installed:
```powershell
python -m pip install "pymongo[srv]" dnspython
```

---

## 📚 Additional Resources

- MongoDB Python Driver: https://pymongo.readthedocs.io/
- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/
- Connection String Format: https://docs.mongodb.com/manual/reference/connection-string/

---

## ✅ Quick Checklist

- [ ] Replace `<db_password>` with actual password
- [ ] Install pymongo: `pip install "pymongo[srv]"`
- [ ] Test connection: `python mongo_helper.py`
- [ ] Add `.env` to `.gitignore`
- [ ] Verify IP whitelist in MongoDB Atlas
- [ ] Test queries work correctly
