# Quick MySQL Start Guide

## 🚀 Fastest Way: Install XAMPP

1. **Download XAMPP** (includes MySQL + phpMyAdmin):
   - https://www.apachefriends.org/download.html
   - Download and install

2. **Start MySQL**:
   - Open "XAMPP Control Panel"
   - Click "Start" next to MySQL
   - ✅ MySQL is now running!

3. **Default Settings**:
   - Username: `root`
   - Password: (usually empty/blank)

4. **Update your app.py**:
   ```python
   app.config['MYSQL_PASSWORD'] = ''  # Empty if no password set
   ```

---

## 🔧 If MySQL is Already Installed

### Start MySQL Service:

**Method 1: Windows Services**
- Press `Win + R`
- Type `services.msc`
- Find "MySQL80" or "MySQL"
- Right-click → Start

**Method 2: Command Line (Run as Administrator)**
```powershell
Start-Service MySQL80
```

**Method 3: XAMPP Control Panel**
- Open XAMPP Control Panel
- Click "Start" next to MySQL

---

## ✅ Verify MySQL is Running

```powershell
# Check if port 3306 is listening
netstat -an | findstr 3306
```

If you see `0.0.0.0:3306` or `127.0.0.1:3306`, MySQL is running!

---

## 📝 Next Steps After MySQL is Running

1. **Create the database**:
   ```bash
   mysql -u root -p < database/bank_db.sql
   ```

2. **Create admin account**:
   ```bash
   python create_default_admin.py
   ```

3. **Start the app**:
   ```bash
   python app.py
   ```

---

## 🆘 Still Having Issues?

Check `MYSQL_SETUP_GUIDE.md` for detailed troubleshooting.

