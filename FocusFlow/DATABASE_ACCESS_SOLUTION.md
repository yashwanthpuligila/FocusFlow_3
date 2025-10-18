# 🔧 FocusFlow Database Access - Complete Solution

## ⚠️ Current Issue
Your backend server is shutting down immediately after starting when run in background mode. This is preventing H2 Console access.

## ✅ Solution: Run Backend in Foreground

### Step 1: Start Backend Server (Keep Terminal Open)

Open a **NEW PowerShell terminal** and run:

```powershell
$env:JAVA_HOME="C:\Program Files\Microsoft\jdk-17.0.16.8-hotspot"
cd y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn spring-boot:run
```

**IMPORTANT:** DO NOT close this terminal! Keep it running in the background.

You should see:
```
Tomcat started on port 8081 (http)
H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:focusflow'
```

---

### Step 2: Access H2 Database Console

Once the backend is running, open your browser and go to:

```
http://localhost:8081/h2-console
```

###  Step 3: Login to Database

Use these credentials in the H2 Console login form:

| Field | Value |
|-------|-------|
| **JDBC URL** | `jdbc:h2:mem:focusflow` |
| **Username** | `sa` |
| **Password** | _(leave empty)_ |
| **Driver Class** | `org.h2.Driver` |

Click **"Connect"**

---

## 📊 Available Tables

Once connected, you'll see these tables:

- **APP_USER** - User accounts (username, password, email, full_name, etc.)
- **CLIENT** - Registered client devices
- **RULE** - Application/website blocking rules

---

## 🔍 Sample SQL Queries

### View all users:
```sql
SELECT * FROM APP_USER;
```

### View all clients:
```sql
SELECT * FROM CLIENT;
```

### View all blocking rules:
```sql
SELECT * FROM RULE;
```

### Count total users:
```sql
SELECT COUNT(*) AS total_users FROM APP_USER;
```

### Find a specific user:
```sql
SELECT * FROM APP_USER WHERE username = 'your_username';
```

### View active rules only:
```sql
SELECT * FROM RULE WHERE enabled = TRUE;
```

---

## 🌐 Alternative: Use REST API

If H2 Console doesn't work, you can access data through REST endpoints:

### Get all users:
```
GET http://localhost:8081/api/auth/users
```

### Login:
```
POST http://localhost:8081/api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Register new user:
```
POST http://localhost:8081/api/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123",
  "email": "newuser@example.com",
  "fullName": "New User"
}
```

---

## 🔧 Troubleshooting

### Backend shuts down immediately
- **Cause:** Running in background mode terminates the process
- **Fix:** Run `mvn spring-boot:run` in a dedicated terminal and KEEP IT OPEN

### Port 8081 already in use
```powershell
# Find process on port 8081
netstat -ano | findstr :8081

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

### H2 Console shows 404 Error
- **Check:** Make sure backend is actually running (`netstat -ano | findstr :8081`)
- **Check:** Use the correct URL: `http://localhost:8081/h2-console` (NOT port 8080)
- **Check:** `spring.h2.console.enabled=true` in `application.properties`

### Can't see any data
- The database is **in-memory** (resets on restart)
- Check if `data.sql` initialization script ran
- Use SQL to insert test data if needed

---

## 💾 Important Notes

1. **In-Memory Database:** H2 database is in-memory, meaning all data is lost when the backend stops
2. **Test Data:** The `data.sql` file in `src/main/resources` contains initialization data
3. **Security:** The generated Spring Security password is shown in terminal logs (look for: "Using generated security password: ...")

---

## 🚀 Quick Start Script

Save this as `start-backend.ps1`:

```powershell
# FocusFlow Backend Starter
$env:JAVA_HOME="C:\Program Files\Microsoft\jdk-17.0.16.8-hotspot"
Set-Location "y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend"
Write-Host "🚀 Starting FocusFlow Backend..." -ForegroundColor Green
Write-Host "📊 H2 Console will be available at: http://localhost:8081/h2-console" -ForegroundColor Cyan
Write-Host "⚠️  Keep this window open!" -ForegroundColor Yellow
mvn spring-boot:run
```

Run it with:
```powershell
.\start-backend.ps1
```

---

**Need help?** Check the terminal output for error messages!
