# MongoDB Connection Guide for FocusFlow

**Date:** October 18, 2025  
**Project:** FocusFlow Admin Backend (Java Spring Boot)

---

## 📂 File Structure - Where Everything Goes

```
focusflow-admin-backend/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── focusflow/
│   │   │           └── admin/
│   │   │               ├── config/           ← MongoDB config classes (if needed)
│   │   │               ├── model/           
│   │   │               │   └── User.java    ← Already using @Document for MongoDB
│   │   │               ├── repo/
│   │   │               │   └── UserRepository.java  ← MongoDB repository
│   │   │               └── service/
│   │   └── resources/
│   │       ├── application.properties  ← ✅ PUT MONGODB CONFIG HERE
│   │       └── application.yml         ← Or here (choose one)
└── pom.xml                            ← Dependencies already added ✅
```

---

## ✅ What's Already Done

Your project already has:
1. ✅ MongoDB dependency in `pom.xml`:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-data-mongodb</artifactId>
   </dependency>
   ```

2. ✅ User model with MongoDB annotations:
   ```java
   @Document(collection = "users")
   public class User {
       @Id
       private String id;
       // ... other fields
   }
   ```

3. ✅ MongoDB repository (MongoRepository):
   - Location: `src/main/java/com/focusflow/admin/repo/UserRepository.java`

---

## 🔧 MongoDB Connection Configuration

### Option 1: Local MongoDB (Recommended for Development)

**File:** `src/main/resources/application.properties`

```properties
# MongoDB Configuration
spring.data.mongodb.uri=mongodb://localhost:27017/focusflow
spring.data.mongodb.database=focusflow
```

### Option 2: MongoDB Atlas (Cloud)

**File:** `src/main/resources/application.properties`

```properties
# MongoDB Atlas Configuration
spring.data.mongodb.uri=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/focusflow?retryWrites=true&w=majority
```

### Option 3: Advanced Configuration (application.yml)

**File:** `src/main/resources/application.yml`

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/focusflow
      # OR for separate configuration:
      host: localhost
      port: 27017
      database: focusflow
      # If authentication required:
      # username: your_username
      # password: your_password
      # authentication-database: admin
```

---

## 🚀 Setup Steps

### Step 1: Install MongoDB

**Option A: MongoDB Community Server (Local)**
```powershell
# Download from: https://www.mongodb.com/try/download/community
# Or use Chocolatey:
choco install mongodb
```

**Option B: MongoDB Atlas (Cloud - Free Tier)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster
4. Get connection string

### Step 2: Start MongoDB (if using local)

```powershell
# Start MongoDB service
net start MongoDB

# OR if installed without service:
mongod --dbpath="C:\data\db"
```

### Step 3: Verify MongoDB is Running

```powershell
# Connect to MongoDB shell
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
```

### Step 4: Configure Connection String

Edit `application.properties`:
```properties
# Add this line (already done for you):
spring.data.mongodb.uri=mongodb://localhost:27017/focusflow
```

### Step 5: Test the Connection

Run your Spring Boot application:
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn spring-boot:run
```

Look for this in the logs:
```
✅ Cluster created with settings {...}
✅ Opened connection [connectionId{localValue:1...}] to localhost:27017
```

---

## 📝 Your Current Database Setup

Your project uses **BOTH** databases:

### 1. **H2 Database** (In-memory)
- **Used for:** JPA entities (`Rule`, `Client`)
- **Configuration:** Already in `application.properties`
- **Console:** http://localhost:8081/h2-console

### 2. **MongoDB**
- **Used for:** User authentication (`User` model)
- **Configuration:** Just added to `application.properties`
- **Collection:** `users`

---

## 🔐 Environment Variables (Production Best Practice)

For production, use environment variables instead of hardcoding credentials:

**File:** `src/main/resources/application.properties`
```properties
spring.data.mongodb.uri=${MONGODB_URI:mongodb://localhost:27017/focusflow}
```

Set environment variable:
```powershell
# Windows
$env:MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/focusflow"

# Or in System Environment Variables
```

---

## 🧪 Testing MongoDB Connection

### Create a Test Endpoint

**File:** `src/main/java/com/focusflow/admin/controller/TestController.java`

```java
package com.focusflow.admin.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/test")
public class TestController {
    
    @Autowired
    private MongoTemplate mongoTemplate;
    
    @GetMapping("/mongodb")
    public String testMongoDB() {
        try {
            String dbName = mongoTemplate.getDb().getName();
            return "✅ Connected to MongoDB: " + dbName;
        } catch (Exception e) {
            return "❌ MongoDB connection failed: " + e.getMessage();
        }
    }
}
```

Test it:
```
http://localhost:8081/api/test/mongodb
```

---

## 🗄️ MongoDB GUI Tools (Optional)

To view your data visually:

1. **MongoDB Compass** (Official)
   - Download: https://www.mongodb.com/products/compass
   - Connection: `mongodb://localhost:27017`

2. **Studio 3T** (Advanced)
   - Download: https://studio3t.com/

3. **VS Code Extension**
   - Install: "MongoDB for VS Code"

---

## 📊 Viewing Your Data

### Using MongoDB Shell (mongosh)
```powershell
# Connect
mongosh

# Switch to your database
use focusflow

# View collections
show collections

# View users
db.users.find().pretty()

# Count users
db.users.countDocuments()
```

### Using MongoDB Compass
1. Open Compass
2. Connect to: `mongodb://localhost:27017`
3. Navigate to `focusflow` database
4. Browse `users` collection

---

## 🐛 Troubleshooting

### Error: "Connection refused"
```
❌ com.mongodb.MongoSocketOpenException: Exception opening socket
```

**Solutions:**
1. Make sure MongoDB is running:
   ```powershell
   net start MongoDB
   # Or: mongod --dbpath="C:\data\db"
   ```

2. Check if port 27017 is open:
   ```powershell
   netstat -an | findstr "27017"
   ```

### Error: "Authentication failed"
```properties
# Add authentication to connection string:
spring.data.mongodb.uri=mongodb://username:password@localhost:27017/focusflow?authSource=admin
```

### Error: "Database doesn't exist"
**Don't worry!** MongoDB creates the database automatically when you insert the first document.

### Connection Timeout
```properties
# Increase timeout in application.properties:
spring.data.mongodb.uri=mongodb://localhost:27017/focusflow?connectTimeoutMS=10000&socketTimeoutMS=10000
```

---

## 📝 Sample Code - Using MongoDB in Your Service

Your `UserRepository` already extends `MongoRepository`, so you can use it like this:

**File:** `src/main/java/com/focusflow/admin/service/UserService.java`

```java
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    // Save user to MongoDB
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    // Find user by username (MongoDB query)
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
    
    // Get all users
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
}
```

---

## 🔄 Migration from H2 to MongoDB (If Needed)

If you want to move all data to MongoDB:

1. Remove H2 dependency from `pom.xml`
2. Convert JPA entities to MongoDB documents:
   ```java
   @Document(collection = "rules")  // Instead of @Entity
   public class Rule {
       @Id
       private String id;  // Instead of Long
       // ... rest of the fields
   }
   ```
3. Change repositories to extend `MongoRepository`

---

## 📚 Additional Resources

- **Spring Data MongoDB Docs:** https://docs.spring.io/spring-data/mongodb/docs/current/reference/html/
- **MongoDB Manual:** https://docs.mongodb.com/manual/
- **MongoDB Atlas Setup:** https://www.mongodb.com/docs/atlas/getting-started/

---

## ✅ Quick Checklist

- [ ] MongoDB installed and running
- [ ] Connection string added to `application.properties`
- [ ] Application builds successfully: `mvn clean install`
- [ ] Application starts: `mvn spring-boot:run`
- [ ] MongoDB connection confirmed in logs
- [ ] Test endpoint returns success
- [ ] Can view data in MongoDB Compass/Shell

---

## 🎯 Next Steps

1. **Start MongoDB:** `net start MongoDB` or `mongod`
2. **Run your app:** `mvn spring-boot:run`
3. **Test signup/login:** Your User model will automatically save to MongoDB
4. **View data:** Use MongoDB Compass or mongosh

Your MongoDB configuration is ready to use! 🚀
