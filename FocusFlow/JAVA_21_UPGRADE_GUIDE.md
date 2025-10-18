# Java 21 Upgrade Guide for FocusFlow

## Overview
This guide outlines the steps to upgrade both FocusFlow projects from Java 17 to Java 21 LTS.

## Projects Updated
1. **focusflow-admin-backend** - Spring Boot backend application
2. **focusflow-student-agent** - Java agent application

## Changes Made

### 1. focusflow-admin-backend/pom.xml
- Updated `<java.version>` from `17` to `21`
- Current Spring Boot version (3.3.2) is compatible with Java 21

### 2. focusflow-student-agent/pom.xml
- Updated `<maven.compiler.release>` from `17` to `21`

## Required Actions

### Step 1: Install Java 21 LTS
You currently have Java 17 installed. You need to install Java 21 to compile and run the projects.

**Option A: Download from Microsoft**
```
https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-21
```

**Option B: Download from Oracle**
```
https://www.oracle.com/java/technologies/downloads/#java21
```

**Option C: Using Windows Package Manager (winget)**
```powershell
winget install Microsoft.OpenJDK.21
```

### Step 2: Set JAVA_HOME Environment Variable
After installing Java 21, set the JAVA_HOME environment variable:

**PowerShell (Current Session):**
```powershell
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-21.0.x-hotspot"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
```

**Windows System Settings (Permanent):**
1. Open System Properties → Environment Variables
2. Create/Update JAVA_HOME to point to Java 21 installation
3. Add `%JAVA_HOME%\bin` to PATH

### Step 3: Verify Java 21 Installation
```powershell
java -version
# Should show: openjdk version "21.0.x"
```

### Step 4: Clean and Rebuild Projects

**For focusflow-admin-backend:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn clean install
```

**For focusflow-student-agent:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-student-agent
mvn clean install
```

## Compatibility Notes

### Spring Boot 3.3.2
- ✅ Fully compatible with Java 21
- Spring Boot 3.x requires Java 17 minimum, supports up to Java 21

### Dependencies
All current dependencies are compatible with Java 21:
- spring-boot-starter-web
- spring-boot-starter-websocket
- spring-boot-starter-security
- spring-boot-starter-data-mongodb
- spring-boot-starter-validation
- spring-boot-starter-actuator
- Java-WebSocket 1.5.6
- jackson-databind 2.17.2

## Java 21 New Features Available

Your projects can now leverage these Java 21 features:

### 1. **Virtual Threads (Preview in 19, Final in 21)**
- Lightweight threads for better concurrency
- Useful for handling WebSocket connections efficiently

### 2. **Pattern Matching for switch**
- Cleaner switch statements with pattern matching

### 3. **Record Patterns**
- Destructuring records in pattern matching

### 4. **Sequenced Collections**
- New interfaces: SequencedCollection, SequencedSet, SequencedMap

### 5. **String Templates (Preview)**
- Better string interpolation

## Testing Recommendations

1. **Run Unit Tests:**
   ```powershell
   mvn test
   ```

2. **Test WebSocket Connections:**
   - Ensure admin backend WebSocket endpoints work correctly
   - Test student agent WebSocket connectivity

3. **Test MongoDB Integration:**
   - Verify database connections and operations

4. **Test Security Features:**
   - Verify authentication and authorization flows

## Rollback Instructions

If you encounter issues, you can rollback to Java 17:

1. **Revert pom.xml changes:**
   - focusflow-admin-backend: Change `<java.version>21</java.version>` back to `17`
   - focusflow-student-agent: Change `<maven.compiler.release>21</maven.compiler.release>` back to `17`

2. **Set JAVA_HOME back to Java 17:**
   ```powershell
   $env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-17.0.16.8-hotspot"
   ```

3. **Rebuild projects:**
   ```powershell
   mvn clean install
   ```

## Next Steps

1. ✅ Update POM files (COMPLETED)
2. ⏳ Install Java 21 JDK
3. ⏳ Update JAVA_HOME environment variable
4. ⏳ Clean and rebuild both projects
5. ⏳ Run tests to verify compatibility
6. ⏳ Update any CI/CD pipelines to use Java 21
7. ⏳ Update README.md with new Java version requirement

## Support

If you encounter any issues during the upgrade:
- Check Spring Boot 3.3.2 release notes
- Review Java 21 migration guide: https://docs.oracle.com/en/java/javase/21/migrate/
- Check for deprecated API usage in your code

## Summary

The Java 21 upgrade is straightforward for your projects:
- ✅ Code changes: Minimal (just POM file updates)
- ✅ Compatibility: Excellent (Spring Boot 3.3.2 fully supports Java 21)
- ✅ Risk: Low (Java 21 is LTS with strong backward compatibility)
- ⚡ Benefits: Performance improvements, new language features, long-term support

---
**Upgrade Status:** Configuration Updated - JDK Installation Required
**Date:** October 18, 2025
