# 🗄️ How to Access Your FocusFlow Database

## Quick Access

**H2 Console URL:** http://localhost:8081/h2-console

---

## 🔐 Connection Settings

When the H2 Console opens, use these settings:

```
Setting           Value
─────────────────────────────────────────
Driver Class:     org.h2.Driver
JDBC URL:         jdbc:h2:mem:focusflow
User Name:        sa
Password:         (leave empty)
```

Click **"Connect"** button to access the database.

---

## 📊 Database Tables

### 1. **app_user** - User Accounts

Stores all registered users (signup/login data).

**Columns:**
- `id` - User ID (auto-increment)
- `username` - Unique username
- `password` - Password (currently plain text)
- `email` - Unique email address
- `full_name` - User's full name
- `active` - Account status (true/false)
- `created_at` - Registration timestamp
- `updated_at` - Last update timestamp

**View all users:**
```sql
SELECT * FROM app_user;
```

**View specific user:**
```sql
SELECT * FROM app_user WHERE username = 'admin';
```

### 2. **rule** - Blocking Rules

Stores app/website blocking rules.

**Columns:**
- `id` - Rule ID
- `type` - BLACKLIST or WHITELIST
- `target_type` - APP or WEBSITE
- `pattern` - App/site to block (e.g., chrome.exe)
- `enabled` - Rule enabled status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

**View all rules:**
```sql
SELECT * FROM rule;
```

**View blocked apps only:**
```sql
SELECT * FROM rule 
WHERE target_type = 'APP' 
AND type = 'BLACKLIST' 
AND enabled = true;
```

### 3. **client** - Connected Clients

Stores information about connected student agents.

**Columns:**
- `id` - Client ID
- `hostname` - Computer name
- `ip` - IP address
- `last_seen` - Last connection time

**View all clients:**
```sql
SELECT * FROM client;
```

---

## 🎯 Useful SQL Queries

### User Management

**Count total users:**
```sql
SELECT COUNT(*) as total_users FROM app_user;
```

**Find user by email:**
```sql
SELECT username, email, full_name 
FROM app_user 
WHERE email = 'test@example.com';
```

**List all active users:**
```sql
SELECT username, email, created_at 
FROM app_user 
WHERE active = true;
```

**Get recently registered users:**
```sql
SELECT username, email, created_at 
FROM app_user 
ORDER BY created_at DESC 
LIMIT 5;
```

### Blocking Rules

**Count blocked apps:**
```sql
SELECT COUNT(*) as blocked_apps 
FROM rule 
WHERE target_type = 'APP' 
AND type = 'BLACKLIST';
```

**List all enabled rules:**
```sql
SELECT pattern, target_type, type 
FROM rule 
WHERE enabled = true;
```

**Add new blocking rule:**
```sql
INSERT INTO rule (type, target_type, pattern, enabled, created_at, updated_at)
VALUES ('BLACKLIST', 'APP', 'spotify.exe', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

**Delete a rule:**
```sql
DELETE FROM rule WHERE pattern = 'spotify.exe';
```

### Database Structure

**Show all tables:**
```sql
SHOW TABLES;
```

**Describe table structure:**
```sql
SHOW COLUMNS FROM app_user;
```

**Get table row count:**
```sql
SELECT 
  (SELECT COUNT(*) FROM app_user) as users,
  (SELECT COUNT(*) FROM rule) as rules,
  (SELECT COUNT(*) FROM client) as clients;
```

---

## 🔄 API Alternative

You can also access data via REST APIs:

### Get All Users
```
GET http://localhost:8081/api/auth/users
```

### Get All Rules
```
GET http://localhost:8081/api/rules
```

### Get All Clients
```
GET http://localhost:8081/api/clients
```

---

## ⚠️ Important Notes

### In-Memory Database
- **Data is temporary** - Lost when backend stops
- **Resets on restart** - Default data reloaded
- **No persistence** - For production, use PostgreSQL/MySQL

### Default Data
When backend starts, it creates:
- **Admin user**: username=`admin`, password=`admin`
- **Sample rule**: Blocks youtube.com

### Security Warning
- **Passwords are NOT hashed** - Stored in plain text
- **For development only** - Not production-ready
- **Should implement BCrypt** - For secure password storage

---

## 💡 Pro Tips

### 1. Export Query Results
In H2 Console, you can export results as:
- CSV
- Excel
- HTML
- XML

### 2. Use Auto-Complete
- Press `Ctrl + Space` for table/column suggestions
- Start typing table names for hints

### 3. Multiple Query Execution
- Separate queries with semicolons
- Click "Run All" to execute multiple queries

### 4. Save Queries
- Bookmark frequently used queries
- Create views for complex queries

### 5. Check Execution Plan
```sql
EXPLAIN SELECT * FROM app_user;
```

---

## 🛠️ Troubleshooting

### Can't Connect to H2 Console
1. Verify backend is running: http://localhost:8081
2. Check browser console for errors (F12)
3. Try clearing browser cache
4. Restart backend server

### Tables Not Showing
1. Check JDBC URL is correct: `jdbc:h2:mem:focusflow`
2. Verify username is `sa` (lowercase)
3. Ensure password field is empty

### Data Not Persisting
- This is expected! H2 is in-memory
- Data resets every backend restart
- To persist data, configure file-based H2 or switch to PostgreSQL

---

## 📚 Additional Resources

- **H2 Documentation:** http://www.h2database.com/html/main.html
- **SQL Tutorial:** https://www.w3schools.com/sql/
- **Your API Docs:** See `AUTHENTICATION_SETUP.md`

---

## 🎯 Quick Start Checklist

- [ ] Backend running on port 8081
- [ ] Open http://localhost:8081/h2-console
- [ ] Enter connection details (JDBC URL, username, password)
- [ ] Click "Connect"
- [ ] Run `SELECT * FROM app_user;`
- [ ] View your data! ✅

---

**Your database is ready to explore! 🎉**

For questions or issues, check the backend terminal logs.
