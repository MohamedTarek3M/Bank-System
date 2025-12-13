# MySQL Setup Guide for Windows

This guide will help you install and run MySQL on Windows for the Bank Management System.

## Option 1: Install MySQL Server (Recommended)

### Method A: MySQL Installer (Easiest)

1. **Download MySQL Installer**
   - Go to: https://dev.mysql.com/downloads/installer/
   - Download "MySQL Installer for Windows" (the larger file, ~400MB)
   - Choose the "Full" or "Developer Default" setup type

2. **Run the Installer**
   - Run the downloaded `.msi` file
   - Choose "Developer Default" or "Server only"
   - Follow the installation wizard
   - **Important**: Remember the root password you set during installation!

3. **Start MySQL Service**
   - The installer usually sets MySQL to start automatically
   - If not, go to Windows Services:
     - Press `Win + R`, type `services.msc`, press Enter
     - Find "MySQL80" or "MySQL" service
     - Right-click → Start

### Method B: XAMPP (Includes MySQL + phpMyAdmin)

1. **Download XAMPP**
   - Go to: https://www.apachefriends.org/download.html
   - Download XAMPP for Windows
   - Install it (usually to `C:\xampp`)

2. **Start MySQL**
   - Open XAMPP Control Panel
   - Click "Start" next to MySQL
   - MySQL will run on port 3306

3. **Default Credentials**
   - Username: `root`
   - Password: (usually empty/blank, or what you set during installation)

### Method C: MySQL via Chocolatey (If you have Chocolatey)

```powershell
choco install mysql
```

---

## Option 2: Check if MySQL is Already Installed

### Check Common Installation Paths:

```powershell
# Check if MySQL is installed in Program Files
Test-Path "C:\Program Files\MySQL"
Test-Path "C:\Program Files (x86)\MySQL"

# Check XAMPP
Test-Path "C:\xampp\mysql"
```

### Check Windows Services:

```powershell
# Run in PowerShell (as Administrator)
Get-Service | Where-Object {$_.Name -like "*mysql*"}
```

---

## Starting MySQL Service

### Method 1: Windows Services (GUI)

1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Find "MySQL80" or "MySQL" service
4. Right-click → Start
5. (Optional) Right-click → Properties → Set "Startup type" to "Automatic"

### Method 2: Command Line (PowerShell as Administrator)

```powershell
# Start MySQL service
Start-Service MySQL80

# Or if service name is different:
Start-Service MySQL

# Check status
Get-Service MySQL80
```

### Method 3: Using MySQL Command Line

If MySQL is in your PATH:

```bash
# Start MySQL (if installed as Windows service)
net start MySQL80

# Or
net start MySQL
```

---

## Verify MySQL is Running

### Test Connection:

```powershell
# Try to connect (if MySQL is in PATH)
mysql -u root -p

# Or test with Python
python -c "import mysql.connector; print('MySQL connector works!')"
```

### Check Port 3306:

```powershell
# Check if port 3306 is listening
netstat -an | findstr 3306
```

---

## Configure Your Bank System

After MySQL is running, update your configuration:

1. **Update `app.py`** (lines 9-12):
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Change this!
   app.config['MYSQL_DB'] = 'bank_db'
   ```

2. **Update `create_default_admin.py`** (line 14):
   ```python
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Change this!
   ```

3. **Create the Database**:
   ```bash
   mysql -u root -p < database/bank_db.sql
   ```
   
   Or manually in MySQL:
   ```sql
   source database/bank_db.sql
   ```

---

## Quick Start Checklist

- [ ] MySQL Server installed
- [ ] MySQL service is running
- [ ] Database `bank_db` created (run `bank_db.sql`)
- [ ] Updated MySQL password in `app.py`
- [ ] Updated MySQL password in `create_default_admin.py`
- [ ] Created admin account (run `create_default_admin.py`)
- [ ] Started Flask app (`python app.py`)

---

## Troubleshooting

### Error: "Can't connect to MySQL server"

**Solutions:**
1. Make sure MySQL service is running
2. Check if MySQL is listening on port 3306
3. Verify username and password are correct
4. Check firewall settings

### Error: "Access denied for user 'root'@'localhost'"

**Solutions:**
1. Reset MySQL root password
2. Or create a new MySQL user:
   ```sql
   CREATE USER 'bankuser'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON bank_db.* TO 'bankuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

### MySQL Not in PATH

**Solution:** Add MySQL to Windows PATH:
1. Find MySQL installation (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
2. Add to System Environment Variables → Path

---

## Alternative: Use SQLite (No Installation Needed)

If you can't install MySQL, I can modify the system to use SQLite instead, which requires no installation. Let me know if you'd like this option!

---

## Need Help?

1. Check MySQL error logs (usually in `C:\ProgramData\MySQL\MySQL Server 8.0\Data\`)
2. Check Windows Event Viewer for MySQL service errors
3. Verify MySQL is listening: `netstat -an | findstr 3306`

