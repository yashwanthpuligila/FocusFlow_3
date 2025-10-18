# 🎯 QUICK START: MongoDB Atlas Connection

## ⚠️ IMPORTANT - Do This First!

Your MongoDB connection code is ready, but you need to **replace the password placeholder**.

---

## 🔐 Step-by-Step Setup

### ✅ Step 1: Get Your MongoDB Password

You should have received this password when you created your MongoDB Atlas user:
- Username: `yashwanthpuligila548`
- Password: `<YOUR_PASSWORD_HERE>`

If you don't remember it:
1. Go to: https://cloud.mongodb.com
2. Navigate to: Database Access
3. Edit user: `yashwanthpuligila548`
4. Reset password

---

### ✅ Step 2: Update the Password

**Option A: Direct Replacement (Quick Test)**

Open: `Y:\Focus_Flow_3\FocusFlow\block_apps\mongo_helper.py`

Find line 9:
```python
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '<db_password>')
```

Replace `<db_password>` with your actual password:
```python
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'YourActualPassword123!')
```

**Option B: Environment Variable (Recommended)**

1. Create file: `Y:\Focus_Flow_3\FocusFlow\block_apps\.env`
   ```
   MONGODB_PASSWORD=YourActualPassword123!
   ```

2. Install python-dotenv:
   ```powershell
   pip install python-dotenv
   ```

3. Update `mongo_helper.py` (add at top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

### ✅ Step 3: Test Connection

```powershell
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python mongo_helper.py
```

**Expected Success Output:**
```
🔌 Testing MongoDB Atlas connection...

✅ Successfully connected to MongoDB Atlas!

📊 Available databases:
  - admin
  - focusflow

📁 Collections in 'focusflow' database:
  - users: 0 documents

👥 Fetching users...
```

---

## 🐛 Common Issues

### Issue 1: "authentication failed"
```
❌ bad auth : authentication failed
```
**Solution:** Password is wrong. Double-check your MongoDB Atlas password.

### Issue 2: "connection timeout"
```
❌ connection timeout
```
**Solutions:**
1. Check MongoDB Atlas → Network Access
2. Add your IP: Click "Add IP Address" → "Add Current IP Address"
3. Or allow all IPs: `0.0.0.0/0` (not recommended for production)

### Issue 3: "DNS name not found"
```
❌ DNS name not found
```
**Solution:** Install dnspython:
```powershell
python -m pip install "pymongo[srv]" dnspython
```

---

## 📂 Your Files

```
block_apps/
├── mongo_helper.py          ← ✅ Updated with your connection code
├── .env.example             ← Template for environment variables
├── MONGODB_PYTHON_SETUP.md  ← Detailed documentation
└── .env                     ← Create this with your password (don't commit!)
```

---

## 🚀 Quick Commands

```powershell
# Test connection
cd Y:\Focus_Flow_3\FocusFlow\block_apps
python mongo_helper.py

# Use in your scripts
python
>>> from mongo_helper import get_database
>>> db = get_database()
>>> db.users.find_one()
```

---

## 🔒 Security Reminder

**NEVER commit your password to Git!**

Add to `.gitignore`:
```
# MongoDB credentials
.env
*.env
```

---

## 📞 Need Help?

1. Check: `MONGODB_PYTHON_SETUP.md` for detailed guide
2. MongoDB Atlas Dashboard: https://cloud.mongodb.com
3. Verify:
   - ✅ Password is correct
   - ✅ IP is whitelisted
   - ✅ User has permissions

---

## ✅ Summary

You have:
- ✅ pymongo with srv support installed
- ✅ Connection code written in `mongo_helper.py`
- ✅ MongoDB Atlas cluster ready
- ⏳ **Need to:** Replace `<db_password>` with actual password

After replacing the password, run `python mongo_helper.py` to test!
