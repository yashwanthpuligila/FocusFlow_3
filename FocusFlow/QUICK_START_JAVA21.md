# Quick Start Guide - Java 21 Upgrade

## ✅ What Was Done

Successfully upgraded both Java projects to Java 21 LTS:

### Files Modified:

1. **focusflow-admin-backend/pom.xml**
   - Java version: 17 → 21
   - Spring Boot: 3.3.2 → 3.4.1

2. **focusflow-student-agent/pom.xml**
   - Maven compiler release: 17 → 21

## ⚠️ Action Required

You currently have Java 17 installed. To complete the upgrade, you need to:

### Step 1: Install Java 21 JDK

**Option A: Using Chocolatey (Recommended for Windows)**
```powershell
choco install openjdk21
```

**Option B: Manual Download**
- Download from: https://adoptium.net/temurin/releases/?version=21
- Choose: Windows x64, .msi installer
- Install and note the installation path (e.g., `C:\Program Files\Eclipse Adoptium\jdk-21.0.5.11-hotspot\`)

### Step 2: Set JAVA_HOME

**PowerShell (Run as Administrator)**:
```powershell
# Set JAVA_HOME
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-21.0.5.11-hotspot", "Machine")

# Update PATH
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$newPath = "C:\Program Files\Eclipse Adoptium\jdk-21.0.5.11-hotspot\bin;$currentPath"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
```

**After setting, restart your terminal and verify:**
```powershell
java -version
# Should show: openjdk version "21.0.x"
```

### Step 3: Build and Test

**Build Admin Backend:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-admin-backend
mvn clean package
```

**Build Student Agent:**
```powershell
cd Y:\Focus_Flow_3\FocusFlow\focusflow-student-agent
mvn clean package
```

## 📝 Changes Summary

| Project | Old Java | New Java | Spring Boot | Status |
|---------|----------|----------|-------------|--------|
| focusflow-admin-backend | 17 | **21** | 3.4.1 | ✅ Updated |
| focusflow-student-agent | 17 | **21** | N/A | ✅ Updated |

## 🚀 Benefits

- **Performance**: 10-15% faster than Java 17
- **Virtual Threads**: Better concurrency with lightweight threads
- **LTS Support**: Supported until September 2031
- **New Features**: Pattern matching, record patterns, sequenced collections

## 📚 Documentation

See `JAVA_21_UPGRADE_SUMMARY.md` for complete details including:
- All new Java 21 features
- Code examples
- Troubleshooting guide
- Rollback instructions

## Need Help?

If you encounter any issues:
1. Check that Java 21 is installed: `java -version`
2. Verify Maven is using Java 21: `mvn -version`
3. Clean and rebuild: `mvn clean install`
4. Check the detailed guide in `JAVA_21_UPGRADE_SUMMARY.md`
