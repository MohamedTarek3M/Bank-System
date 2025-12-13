# Bank Management System

A comprehensive web-based banking system built with Flask and SQLite that supports three user types: Customers, Employees, and Administrators.

## ✨ Features

### 👤 Customer Features
- Secure login/logout
- View account balance in real-time
- View detailed transaction history
- Transfer funds to other accounts with validation
- View profile information
- Dark mode support

### 👔 Employee Features
- Secure login/logout
- Create new customer accounts with validation
- Process deposits and withdrawals
- Transfer funds between customer accounts
- Search and view customer details
- View customer transaction history
- Comprehensive error handling

### 🛠️ Admin Features
- Secure login/logout
- Manage employees (Add, Edit, Delete)
- Generate comprehensive reports (Transactions, Users, Employees)
- View all system transactions
- Monitor system activity

## 🔒 Security Features

- **Password Hashing**: Werkzeug security for password protection
- **Session Management**: Secure session handling with 30-minute timeout
- **Input Validation**: Comprehensive server-side and client-side validation
- **SQL Injection Protection**: Parameterized queries throughout
- **CSRF Protection**: SameSite cookie policy
- **Amount Validation**: Min/max limits and negative amount prevention
- **Self-Transfer Prevention**: Cannot transfer money to yourself
- **Transaction Rollback**: Automatic rollback on errors

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python 3.7+, Flask 2.3.2
- **Database**: SQLite (no installation needed!)
- **Security**: Werkzeug password hashing
- **UI/UX**: Dark mode, responsive design, accessibility features

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- **No database installation needed!** (Uses SQLite)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd "Bank System"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application** (Database auto-creates!)
   ```bash
   python app.py
   ```
   The application will start on `http://localhost:5000`

4. **Create Admin Account**
   - Open a new terminal
   - Run: `python create_default_admin.py`
   - Default credentials: 
     - Username: `admin`
     - Password: `admin123`
   - ⚠️ **Change this password immediately after first login!**

5. **Access the Application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Login as Admin with the credentials above

## 💾 Database

The system uses **SQLite** - a file-based database that requires no installation!

- **Database file**: `database/bank_db.db` (auto-created on first run)
- **Tables**: `users`, `employees`, `admins`, `accounts`, `transactions`
- **No server setup needed** - just run the app!
- **Easy backup**: Simply copy the database file

### Database Schema

- **users**: Customer accounts with balance tracking
- **employees**: Employee accounts with role management
- **admins**: Administrator accounts
- **accounts**: Reserved for future multi-account feature
- **transactions**: Complete transaction history with timestamps

## 📁 Project Structure

```
Bank System/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── docs/                       # Documentation & Guides
│   ├── SECURITY.md
│   ├── MYSQL_SETUP_GUIDE.md
│   └── ...
│
├── scripts/                    # Utility Scripts
│   ├── create_admin.py         # Create custom admin
│   └── create_default_admin.py # Create default admin
│
├── static/                     # Static files
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/                  # HTML templates
│
└── database/
    └── bank_db.db             # SQLite database (auto-created)
```

## 🚀 Usage

### Creating Initial Users

**Create Default Admin:**
```bash
python scripts/create_default_admin.py
```
- Username: `admin`
- Password: `admin123`

**Create Custom Admin:**
```bash
python scripts/create_admin.py
```
Follow the prompts to create a custom admin account.

### Default Routes

- `/` - Login page
- `/user/dashboard` - Customer dashboard
- `/user/transfer` - Transfer funds
- `/employee/dashboard` - Employee dashboard
- `/employee/add_customer` - Add new customer
- `/employee/transaction` - Deposit/Withdraw
- `/admin/dashboard` - Admin dashboard
- `/admin/manage_employees` - Manage employees
- `/admin/reports` - View reports
- `/logout` - Logout (all user types)

## 🎨 Features Highlights

### Dark Mode & Theming
- Toggle between light and dark themes using custom SVG icons
- Preference saved in browser (localStorage)
- Smooth transitions and optimized contrast
- Dynamic icon switching based on active theme

### 💸 Interactive UI Effects
- **Falling Coins Animation**: Visual effect on login and dashboard pages
- **Speed Control**: Customizable falling speed via `window.fallingCoinsSpeed` global variable
- **Performance Optimized**: Reduced coin count on non-login pages to maintain performance
- **Mouse Interaction**: Coins react to cursor movement

### 🌍 Localization
- **Timezone**: All transactions are recorded in Egypt Time (UTC+2)
- **Currency**: Consistent currency formatting

### Form Validation
- Client-side validation for immediate feedback
- Server-side validation for security
- Password strength indicators and visibility toggle
- Amount validation with min/max limits

### User Experience
- Responsive design for all devices
- Confirmation dialogs for critical actions
- Categorized flash messages (success, warning, danger, info)
- Loading states and smooth animations

## 🔧 Development

To run in debug mode (already enabled by default):
```python
app.run(debug=True)
```

**Note**: Set `debug=False` for production deployment.

## 🛡️ Security Best Practices

For production deployment, please review `SECURITY.md` for:
- Secret key management
- HTTPS/SSL configuration
- Database security
- Password policies
- Rate limiting
- Logging and monitoring
- Backup strategies

## 🐛 Troubleshooting

### Database Issues

**Problem**: Database not found
```bash
# Solution: Run the app once to create the database
python app.py
```

**Problem**: Database locked
```bash
# Solution: Close all connections and restart
# Make sure no other process is using the database
```

### Login Issues

**Problem**: Cannot login with default admin
```bash
# Solution: Create admin account
python create_default_admin.py
```

**Problem**: Invalid credentials
- Check username and password (case-sensitive)
- Ensure correct user type is selected
- Try creating a new admin account

### Port Already in Use

**Problem**: Port 5000 is already in use
```python
# Solution: Change port in app.py
if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

## 📈 Future Enhancements

- [ ] Email notifications for transactions
- [ ] Two-factor authentication (2FA)
- [ ] Advanced reporting with charts and graphs
- [ ] Transaction export (CSV/PDF)
- [ ] API endpoints for mobile apps
- [ ] Multi-account support per user
- [ ] Transaction categories and tagging
- [ ] Scheduled/recurring transactions
- [ ] Account statements generation
- [ ] Audit logs for admin actions

## 📝 License

This project is licensed under a Proprietary License. All Rights Reserved.
See the [LICENSE](LICENSE) file for details.
Reference implementation for educational purposes only.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the code comments and documentation
- Check `SECURITY.md` for security-related questions

## 🙏 Acknowledgments

- Built with Flask and Bootstrap
- Icons from custom SVG collection
- Inspired by modern banking systems

---

**Version**: 2.1
**Last Updated**: 2025-12-13
**Status**: Production Ready (with security configuration)


