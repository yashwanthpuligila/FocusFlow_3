# 🔴 MongoDB Authentication Failed - Troubleshooting Guide

## ❌ Current Error
```
bad auth : authentication failed
```

This means the username/password combination is incorrect.

---

## 🔧 How to Fix

### Option 1: Reset Your MongoDB Atlas Password (Recommended)

**Step 1:** Go to MongoDB Atlas
- URL: https://cloud.mongodb.com
- Login to your account

**Step 2:** Navigate to Database Access
1. Click on "Database Access" in the left sidebar
2. Find user: `yashwanthpuligila548`
3. Click "Edit" button

**Step 3:** Reset Password
1. Click "Edit Password"
2. Choose "Autogenerate Secure Password" OR set a custom password
3. **COPY THE PASSWORD** - You won't see it again!
4. Click "Update User"

**Step 4:** Update Your Code
Replace the password in `mongo_helper.py` line 11:
```python
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'YOUR_NEW_PASSWORD_HERE')
```

---

### Option 2: Check Current Password

The password you tried: `yashwanth123!`

**Common issues:**
- ❌ Password has been changed
- ❌ Password was different when you created the user
- ❌ Special characters not entered correctly

**To verify:**
1. Go to MongoDB Atlas → Database Access
2. Check if the user exists: `yashwanthpuligila548`
3. If user doesn't exist, create a new one

---

### Option 3: Create a New Database User

**Step 1:** MongoDB Atlas → Database Access → "+ ADD NEW DATABASE USER"

**Step 2:** Fill in details:
- Authentication Method: Password
- Username: `yashwanth` (or keep `yashwanthpuligila548`)
- Password: Click "Autogenerate Secure Password" and COPY IT
- Database User Privileges: "Atlas admin" or "Read and write to any database"

**Step 3:** Click "Add User"

**Step 4:** Update your connection string with the new username/password

---

## 🌐 Check Network Access

Your IP address must be whitelisted in MongoDB Atlas.

**Step 1:** MongoDB Atlas → Network Access

**Step 2:** Check if your IP is listed

**Step 3:** If not, click "+ ADD IP ADDRESS"
- Option A: "Add Current IP Address" (secure)
- Option B: "Allow Access from Anywhere" (0.0.0.0/0) - for testing only!

**Step 4:** Click "Confirm"

---

## 🧪 Test with MongoDB Compass (GUI Tool)

Download MongoDB Compass to test your connection:
- URL: https://www.mongodb.com/products/compass

**Test Connection:**
```
mongodb+srv://yashwanthpuligila548:YOUR_PASSWORD@cluster1.p9g3qdo.mongodb.net/
```

If Compass connects, your credentials are correct!

---

## 📝 Update Code After Getting Correct Password

### Method 1: Direct in Code (Quick Test)
```python
# In mongo_helper.py, line 11:
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'correct_password_here')
```

### Method 2: Environment Variable (Best Practice)

**PowerShell:**
```powershell
$env:MONGODB_PASSWORD="correct_password_here"
python mongo_helper.py
```

**Or create `.env` file:**
```bash
# block_apps/.env
MONGODB_PASSWORD=correct_password_here
```

Then install and use:
```powershell
pip install python-dotenv
```

Update `mongo_helper.py` to load .env:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this right after imports
```

---

## ✅ Verification Steps

1. ✅ User exists in MongoDB Atlas → Database Access
2. ✅ Password is correct (test with MongoDB Compass)
3. ✅ IP is whitelisted in MongoDB Atlas → Network Access
4. ✅ User has correct permissions (Read/Write access)
5. ✅ Password is URL-encoded in code (already done)

---

## 🎯 Quick Command Reference

### PowerShell (Windows)
```powershell
# Set password for current session
$env:MONGODB_PASSWORD="your_password"

# Test connection
python mongo_helper.py

# Check if variable is set
$env:MONGODB_PASSWORD
```

### Command Line Test
```powershell
# Test with mongosh (if installed)
mongosh "mongodb+srv://yashwanthpuligila548:password@cluster1.p9g3qdo.mongodb.net/"
```

---

## 📞 Next Steps

1. **Go to MongoDB Atlas**: https://cloud.mongodb.com
2. **Check Database Access**: Verify user exists
3. **Reset Password**: Generate new password and copy it
4. **Update Code**: Replace password in `mongo_helper.py`
5. **Test Again**: Run `python mongo_helper.py`

---

## 🔒 Password Requirements

MongoDB Atlas passwords must:
- Be at least 8 characters long
- Contain at least one letter
- Contain at least one number

**Special characters** like `!@#$%^&*` need to be:
- URL-encoded in connection strings
- Entered correctly (case-sensitive)

---

## 💡 Pro Tip

If you're still having issues, try creating a **simple password** first (like `Password123`) just to test the connection, then change it to a secure password later.

---

## 📊 Your Connection Details

- **Cluster**: cluster1.p9g3qdo.mongodb.net
- **Username**: yashwanthpuligila548
- **Database**: focusflow
- **Current Status**: ❌ Authentication failed
- **Action Required**: Update password

Once you get the correct password from MongoDB Atlas and update it in the code, the connection should work! 🚀
