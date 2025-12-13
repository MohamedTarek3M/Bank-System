# How to Create an Admin Account

There are **3 ways** to create an admin account:

## Method 1: Using Python Script (Recommended) ⭐

### Step 1: Make sure MySQL is running
- Start your MySQL server
- Ensure the database `bank_db` exists (run `database/bank_db.sql` first if needed)

### Step 2: Update MySQL password (if needed)
- Open `create_default_admin.py`
- Update line 14 with your MySQL password:
  ```python
  app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
  ```

### Step 3: Run the script
```bash
python create_default_admin.py
```

**Default credentials created:**
- Username: `admin`
- Password: `admin123`

---

## Method 2: Using Interactive Python Script

For custom admin credentials:

```bash
python create_admin.py
```

This will prompt you for:
- Username
- Password
- Full Name

---

## Method 3: Manual SQL Insert (Advanced)

### Step 1: Generate password hash
Run this in Python:
```python
from werkzeug.security import generate_password_hash
password = input("Enter password: ")
print(generate_password_hash(password))
```

### Step 2: Insert into database
```sql
USE bank_db;

INSERT INTO admins (username, password, full_name) 
VALUES ('admin', 'paste_hashed_password_here', 'System Administrator');
```

---

## Troubleshooting

### Error: "Can't connect to server"
- **Solution**: Make sure MySQL server is running
  - Windows: Check Services, start MySQL service
  - Or run: `net start MySQL` (as administrator)

### Error: "Unknown database 'bank_db'"
- **Solution**: Create the database first:
  ```bash
  mysql -u root -p < database/bank_db.sql
  ```

### Error: "Access denied"
- **Solution**: Check MySQL username and password in the script
- Update `create_default_admin.py` line 14 with correct password

---

## After Creating Admin

1. Start the Flask app:
   ```bash
   python app.py
   ```

2. Go to: `http://localhost:5000`

3. Login with:
   - User Type: **Admin**
   - Username: `admin`
   - Password: `admin123`

4. **IMPORTANT**: Change the password after first login for security!

---

## Quick Start (If MySQL is Running)

```bash
# 1. Create database (if not exists)
mysql -u root -p < database/bank_db.sql

# 2. Create admin account
python create_default_admin.py

# 3. Start the app
python app.py
```

