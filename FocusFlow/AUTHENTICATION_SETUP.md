# Authentication Setup Guide

## ✅ What Was Created

Successfully added signup and login functionality to FocusFlow with H2 database storage!

## 📁 Files Created/Modified

### Frontend (React)
1. **`src/pages/Login.js`** - Login page component
2. **`src/pages/Signup.js`** - Signup/registration page component
3. **`src/pages/Auth.css`** - Styles for authentication pages
4. **`src/utils/authService.js`** - Authentication utility functions
5. **`src/pages/Home.js`** - Updated to show login/logout buttons
6. **`src/App.js`** - Added routes for /login and /signup

### Backend (Spring Boot)
Your backend already has:
- ✅ `AuthController.java` - Login and register endpoints
- ✅ `UserService.java` - User authentication logic
- ✅ `User.java` - User model/entity
- ✅ `UserRepository.java` - Database operations
- ✅ H2 Database - In-memory database for storing users

## 🗄️ Database Information

### Database Type
- **H2 In-Memory Database** (configured in `application.properties`)
- Location: `jdbc:h2:mem:focusflow`
- Console: http://localhost:8081/h2-console (when backend is running)

### User Table Schema
```sql
CREATE TABLE app_user (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  full_name VARCHAR(255),
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Default Admin Account
```
Username: admin
Password: admin
Email: admin@focusflow.com
```

## 🚀 How to Use

### Step 1: Start the Backend
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn spring-boot:run
```
Backend will run on: http://localhost:8081

### Step 2: Start the Frontend
```powershell
cd Y:\Focus_Flow_3\FocusFlow\frontend
npm start
```
Frontend will run on: http://localhost:3000

### Step 3: Access the Application

1. **Home Page**: http://localhost:3000
   - See Login/Signup buttons in top-right

2. **Sign Up**: http://localhost:3000/signup
   - Create a new account
   - All fields are required
   - Password must be at least 4 characters

3. **Login**: http://localhost:3000/login
   - Use your credentials or the default admin account

## 📋 Features

### Signup Page
- ✅ Full name, username, email, password fields
- ✅ Password confirmation validation
- ✅ Email format validation
- ✅ Duplicate username/email checking
- ✅ Auto-login after successful registration
- ✅ Error messages for validation failures

### Login Page
- ✅ Username and password fields
- ✅ Authentication with backend API
- ✅ Session storage using localStorage
- ✅ Error handling for invalid credentials
- ✅ Auto-redirect to home after login

### Home Page Updates
- ✅ Shows Login/Signup buttons when not authenticated
- ✅ Shows username and Logout button when authenticated
- ✅ Personalized welcome message

## 🔐 API Endpoints

### Register New User
```http
POST http://localhost:8081/api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123",
  "email": "john@example.com",
  "fullName": "John Doe"
}
```

### Login User
```http
POST http://localhost:8081/api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}
```

### Get All Users (for testing)
```http
GET http://localhost:8081/api/auth/users
```

## 🎨 UI Features

### Authentication Pages Styling
- Beautiful gradient background (purple to blue)
- Smooth animations and transitions
- Responsive design for mobile devices
- Form validation with visual feedback
- Error messages with shake animation
- Loading states for better UX

## 📊 View Database Contents

### Access H2 Console
1. Make sure backend is running
2. Go to: http://localhost:8081/h2-console
3. Use these settings:
   - JDBC URL: `jdbc:h2:mem:focusflow`
   - Username: `sa`
   - Password: (leave empty)
4. Click "Connect"

### Query Users
```sql
SELECT * FROM app_user;
```

## 🔧 Testing Instructions

### Test Signup Flow
1. Go to http://localhost:3000/signup
2. Fill in all fields:
   - Full Name: Test User
   - Username: testuser
   - Email: test@example.com
   - Password: test1234
   - Confirm Password: test1234
3. Click "Sign Up"
4. Should redirect to home with personalized message

### Test Login Flow
1. Log out if currently logged in
2. Go to http://localhost:3000/login
3. Enter credentials:
   - Username: testuser
   - Password: test1234
4. Click "Login"
5. Should redirect to home with username displayed

### Test Logout
1. Click "Logout" button in top-right
2. Should show Login/Signup buttons again

## ⚠️ Important Notes

### Password Security
**CURRENT STATE**: Passwords are stored in **plain text** (not hashed)

**FOR PRODUCTION**: You should implement password hashing using BCrypt:

```java
// In UserService.java
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

// When saving user
user.setPassword(passwordEncoder.encode(request.password));

// When validating
if (!passwordEncoder.matches(request.password, user.getPassword())) {
    // Invalid password
}
```

### Database Persistence
**CURRENT STATE**: H2 in-memory database (data lost on restart)

**FOR PRODUCTION**: Switch to PostgreSQL, MySQL, or file-based H2:

```properties
# File-based H2 (persists on disk)
spring.datasource.url=jdbc:h2:file:./data/focusflow

# Or PostgreSQL
spring.datasource.url=jdbc:postgresql://localhost:5432/focusflow
spring.datasource.username=postgres
spring.datasource.password=yourpassword
```

## 🎯 Next Steps

### Recommended Enhancements
1. **Password Hashing**: Implement BCrypt for secure password storage
2. **JWT Tokens**: Add token-based authentication instead of localStorage
3. **Email Verification**: Send verification email on signup
4. **Password Reset**: Add "Forgot Password" functionality
5. **Persistent Database**: Switch to PostgreSQL or MySQL
6. **Session Management**: Implement proper session handling
7. **Role-Based Access**: Add user roles (admin, student, etc.)
8. **Profile Page**: Let users update their information

### Optional Features
- Social login (Google, GitHub)
- Two-factor authentication
- Password strength meter
- Remember me functionality
- Account deletion
- Privacy settings

## 🐛 Troubleshooting

### Backend Not Starting
```powershell
# Check if port 8081 is already in use
netstat -ano | findstr :8081

# Kill process if needed
taskkill /PID <PID> /F
```

### Frontend Can't Connect
- Make sure backend is running on port 8081
- Check CORS settings in `CorsConfig.java`
- Verify axios is installed: `npm install axios`

### Login/Signup Not Working
1. Check browser console for errors (F12)
2. Verify backend logs for error messages
3. Test API endpoints directly using Postman
4. Clear localStorage: `localStorage.clear()`

## 📝 Code Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.js        # Login page
│   │   ├── Signup.js       # Signup page
│   │   ├── Auth.css        # Auth styling
│   │   └── Home.js         # Updated home
│   ├── utils/
│   │   └── authService.js  # Auth utilities
│   └── App.js              # Routes

backend/
└── src/main/java/com/focusflow/admin/
    ├── controller/
    │   └── AuthController.java
    ├── service/
    │   └── UserService.java
    ├── model/
    │   └── User.java
    ├── repo/
    │   └── UserRepository.java
    └── dto/
        ├── LoginRequest.java
        ├── RegisterRequest.java
        └── AuthResponse.java
```

---

**🎉 Your authentication system is now ready to use!**

All user accounts are stored in the H2 database and persist during the application runtime.
