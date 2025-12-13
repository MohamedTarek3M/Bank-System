# SQLite Quick Start Guide

🎉 **Great news!** The system now uses SQLite - **no installation needed!**

## ✅ What Changed

- ✅ No MySQL installation required
- ✅ Database is automatically created
- ✅ All features work the same
- ✅ Simpler setup process

## 🚀 Quick Start (3 Steps)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App (Database auto-creates!)
```bash
python app.py
```
The database will be automatically created in `database/bank_db.db`

### Step 3: Create Admin Account
Open a **new terminal** (keep app.py running) and run:
```bash
python create_default_admin.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### Step 4: Access the System
1. Open browser: `http://localhost:5000`
2. Login as **Admin**
3. Use credentials above

## 📁 Database Location

The database file is located at:
```
database/bank_db.db
```

You can:
- ✅ View it with any SQLite browser (DB Browser for SQLite)
- ✅ Backup by copying the file
- ✅ Delete it to reset the system (it will recreate on next run)

## 🔧 Creating Custom Admin

For custom admin credentials:
```bash
python create_admin.py
```

## 🆘 Troubleshooting

### "Database not found" error
- Make sure you ran `python app.py` at least once
- The database is created automatically on first run

### "Database is locked" error
- Close any other programs using the database
- Make sure only one instance of app.py is running

### Reset Database
- Stop the app
- Delete `database/bank_db.db`
- Run `python app.py` again (database recreates)
- Run `python create_default_admin.py` again

## ✨ Benefits of SQLite

- ✅ No server installation
- ✅ No configuration needed
- ✅ Database is a single file
- ✅ Easy to backup (just copy the file)
- ✅ Perfect for development
- ✅ Works on Windows, Mac, Linux

## 📝 Next Steps

1. ✅ System is ready to use!
2. Create employees from Admin dashboard
3. Create customers from Employee dashboard
4. Start using the system!

---

**That's it!** No MySQL setup needed. Just run and go! 🎉

---
*Licensed under Proprietary License. All Rights Reserved.*

