# 📍 Quick Reference: Where to Put MongoDB Code

## For Your Java Spring Boot Project

```
┌─────────────────────────────────────────────────────────────┐
│                    focusflow-admin-backend                   │
└─────────────────────────────────────────────────────────────┘

📁 src/main/resources/
  │
  ├── 📄 application.properties  ← ✅ PUT MONGODB CONFIG HERE
  │   └── Add this line:
  │       spring.data.mongodb.uri=mongodb://localhost:27017/focusflow
  │
  └── 📄 application.yml  ← OR here (don't use both)
      └── Add this:
          spring:
            data:
              mongodb:
                uri: mongodb://localhost:27017/focusflow

📁 src/main/java/com/focusflow/admin/
  │
  ├── 📁 model/
  │   └── 📄 User.java  ← ✅ ALREADY CONFIGURED (has @Document)
  │       @Document(collection = "users")
  │       public class User { ... }
  │
  ├── 📁 repo/
  │   └── 📄 UserRepository.java  ← ✅ ALREADY CONFIGURED (MongoRepository)
  │       public interface UserRepository extends MongoRepository<User, String>
  │
  ├── 📁 service/
  │   └── 📄 UserService.java  ← ✅ ALREADY USING MongoDB
  │       // Uses userRepository.save(), .findAll(), etc.
  │
  └── 📁 config/  ← Optional: Custom MongoDB config (if needed)
      └── 📄 MongoConfig.java  ← Only create if you need custom settings
```

---

## What You Need to Do (3 Simple Steps)

### ✅ Step 1: Install MongoDB
```powershell
# Download and install from:
https://www.mongodb.com/try/download/community

# Or use Chocolatey:
choco install mongodb
```

### ✅ Step 2: Start MongoDB
```powershell
# Start MongoDB service
net start MongoDB

# OR run manually:
mongod --dbpath="C:\data\db"
```

### ✅ Step 3: Configuration Already Done!
Your `application.properties` file already has:
```properties
spring.data.mongodb.uri=mongodb://localhost:27017/focusflow
```

That's it! Your code is already written, just need MongoDB running.

---

## 🚫 What You DON'T Need

❌ **No JavaScript/Node.js code** - Your backend is Java
❌ **No npm packages** - You use Maven (pom.xml)
❌ **No database.js file** - Spring Boot handles connections
❌ **No mongoose** - Spring Data MongoDB is already included

---

## ✅ What You Already Have

✅ MongoDB dependency in `pom.xml`
✅ User model with `@Document` annotation
✅ UserRepository extending `MongoRepository`
✅ UserService using the repository
✅ Connection string in `application.properties`

---

## 🎯 Just Run Your App!

```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn spring-boot:run
```

MongoDB will connect automatically when your app starts.

---

## 📊 View Your MongoDB Data

### Option 1: MongoDB Compass (GUI)
1. Download: https://www.mongodb.com/products/compass
2. Connect to: `mongodb://localhost:27017`
3. View database: `focusflow`
4. View collection: `users`

### Option 2: MongoDB Shell
```powershell
mongosh
use focusflow
db.users.find()
```

---

## 🔍 Where Each File Type Goes

| What | Where | Already Done? |
|------|-------|---------------|
| MongoDB connection URL | `application.properties` | ✅ YES |
| User data model | `User.java` | ✅ YES |
| Database operations | `UserRepository.java` | ✅ YES |
| Business logic | `UserService.java` | ✅ YES |
| API endpoints | `AuthController.java` | ✅ YES |
| Dependencies | `pom.xml` | ✅ YES |

---

## 📝 Summary

**You don't need to create any new files!**

Your Java Spring Boot project is already configured for MongoDB.

Just:
1. Install MongoDB
2. Start MongoDB service
3. Run your Spring Boot app

Everything else is already coded! 🚀
