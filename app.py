from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import secrets
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Generate a secure random secret key
app.secret_key = secrets.token_hex(32)

# Session configuration for security
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Constants
DATABASE = 'database/bank_db.db'
MIN_TRANSFER_AMOUNT = 0.01
MAX_TRANSFER_AMOUNT = 1000000.00
MIN_PASSWORD_LENGTH = 6
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,50}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Egypt Timezone (UTC+2) - Helper function
def get_egypt_time():
    """Returns the current time in Egypt (UTC+2)."""
    return datetime.now(timezone.utc) + timedelta(hours=2)

# Helper Functions
def validate_amount(amount_str):
    """
    Validate and convert amount string to Decimal.
    
    Args:
        amount_str: String representation of amount
        
    Returns:
        Decimal: Validated amount
        
    Raises:
        ValueError: If amount is invalid
    """
    try:
        amount = Decimal(str(amount_str))
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount < MIN_TRANSFER_AMOUNT:
            raise ValueError(f"Amount must be at least ${MIN_TRANSFER_AMOUNT}")
        if amount > MAX_TRANSFER_AMOUNT:
            raise ValueError(f"Amount cannot exceed ${MAX_TRANSFER_AMOUNT:,.2f}")
        return amount
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Invalid amount: {str(e)}")

def validate_username(username):
    """
    Validate username format.
    
    Args:
        username: Username string to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If username is invalid
    """
    if not username or not USERNAME_PATTERN.match(username):
        raise ValueError("Username must be 3-50 characters (letters, numbers, underscore only)")
    return True

def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If email is invalid
    """
    if not email or not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email format")
    return True

def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If password is too weak
    """
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    return True

def get_db():
    """
    Get database connection with row factory.
    
    Returns:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """Initialize the database with tables."""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            balance DECIMAL(10,2) DEFAULT 0.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            role VARCHAR(50)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100)
        )
    ''')
    
    # Note: accounts table reserved for future multi-account feature
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            acc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            acc_type VARCHAR(50),
            balance DECIMAL(10,2) DEFAULT 0.0,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emp_id INTEGER,
            trans_type VARCHAR(50),
            amount DECIMAL(10,2),
            trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# ---------------------------
# Home / Login
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Handle user login for all user types (user, employee, admin).
    
    Returns:
        Redirect to appropriate dashboard or login page with error
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user_type = request.form.get("user_type", "")

        if not username or not password or not user_type:
            flash("All fields are required!", "danger")
            return render_template("login.html")

        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            if user_type == "user":
                cursor.execute("SELECT * FROM users WHERE username=?", (username,))
                user = cursor.fetchone()
                if user and check_password_hash(user[2], password):
                    session['user_id'] = user[0]
                    session.permanent = True
                    flash(f"Welcome back, {user[3]}!", "success")
                    return redirect(url_for("user_dashboard"))
                else:
                    flash("Invalid username or password!", "danger")
                    
            elif user_type == "employee":
                cursor.execute("SELECT * FROM employees WHERE username=?", (username,))
                emp = cursor.fetchone()
                if emp and check_password_hash(emp[2], password):
                    session['emp_id'] = emp[0]
                    session.permanent = True
                    flash(f"Welcome back, {emp[3]}!", "success")
                    return redirect(url_for("employee_dashboard"))
                else:
                    flash("Invalid username or password!", "danger")
                    
            elif user_type == "admin":
                cursor.execute("SELECT * FROM admins WHERE username=?", (username,))
                admin = cursor.fetchone()
                if admin and check_password_hash(admin[2], password):
                    session['admin_id'] = admin[0]
                    session.permanent = True
                    flash(f"Welcome back, {admin[3]}!", "success")
                    return redirect(url_for("admin_dashboard"))
                else:
                    flash("Invalid username or password!", "danger")
            else:
                flash("Invalid user type!", "danger")
                
        except Exception as e:
            flash(f"An error occurred during login. Please try again.", "danger")
            print(f"Login error: {str(e)}")  # Log for debugging
        finally:
            if conn:
                conn.close()
                
    return render_template("login.html")

# ---------------------------
# Dashboards
# ---------------------------
@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (session["user_id"],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY trans_date DESC LIMIT 10", (session["user_id"],))
        transactions = cursor.fetchall()
        conn.close()
        return render_template("user_dashboard.html", user=user, transactions=transactions)
    return redirect(url_for("login"))

@app.route("/user/transfer", methods=["GET", "POST"])
def transfer():
    """
    Handle fund transfers between user accounts.
    
    Returns:
        Redirect to dashboard on success or transfer page with errors
    """
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        recipient = request.form.get("recipient", "").strip()
        amount_str = request.form.get("amount", "")
        user_id = session["user_id"]
        
        conn = None
        try:
            # Validate inputs
            if not recipient:
                flash("Recipient username is required!", "danger")
                return redirect(url_for("transfer"))
                
            amount = validate_amount(amount_str)
            
            conn = get_db()
            cursor = conn.cursor()
            
            # Get sender info
            cursor.execute("SELECT user_id, username, balance FROM users WHERE user_id=?", (user_id,))
            sender = cursor.fetchone()
            
            if not sender:
                flash("Sender account not found!", "danger")
                return redirect(url_for("transfer"))
            
            # Prevent self-transfer
            if sender[1] == recipient:
                flash("You cannot transfer money to yourself!", "warning")
                return redirect(url_for("transfer"))
            
            # Get receiver info
            cursor.execute("SELECT user_id, balance FROM users WHERE username=?", (recipient,))
            receiver = cursor.fetchone()
            
            if not receiver:
                flash("Recipient not found!", "danger")
                return redirect(url_for("transfer"))
            
            sender_balance = Decimal(str(sender[2]))
            receiver_balance = Decimal(str(receiver[1]))
            
            # Check sufficient balance
            if amount > sender_balance:
                flash(f"Insufficient balance! Your balance: ${sender_balance:.2f}", "danger")
                return redirect(url_for("transfer"))
            
            # Perform transfer with transaction
            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount
            
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", 
                         (float(new_sender_balance), sender[0]))
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", 
                         (float(new_receiver_balance), receiver[0]))
            
            # Record transactions
            egypt_now = get_egypt_time()
            cursor.execute(
                "INSERT INTO transactions (user_id, emp_id, trans_type, amount, trans_date) VALUES (?,NULL,'Transfer Out',?,?)",
                (sender[0], float(amount), egypt_now)
            )
            cursor.execute(
                "INSERT INTO transactions (user_id, emp_id, trans_type, amount, trans_date) VALUES (?,NULL,'Transfer In',?,?)",
                (receiver[0], float(amount), egypt_now)
            )
            
            conn.commit()
            flash(f"Transfer successful! ${amount:.2f} sent to {recipient}", "success")
            return redirect(url_for("user_dashboard"))
            
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("transfer"))
        except Exception as e:
            if conn:
                conn.rollback()
            flash("An error occurred during transfer. Please try again.", "danger")
            print(f"Transfer error: {str(e)}")
            return redirect(url_for("transfer"))
        finally:
            if conn:
                conn.close()
                
    # GET request - show transfer form
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (session["user_id"],))
        user = cursor.fetchone()
        balance = user[0] if user else 0
        return render_template("transfer.html", balance=balance)
    except Exception as e:
        print(f"Error loading transfer page: {str(e)}")
        return render_template("transfer.html", balance=0)
    finally:
        if conn:
            conn.close()


@app.route("/employee/dashboard")
def employee_dashboard():
    if "emp_id" in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE emp_id=?", (session["emp_id"],))
        employee = cursor.fetchone()
        conn.close()
        return render_template("employee_dashboard.html", employee=employee)
    return redirect(url_for("login"))

@app.route("/employee/add_customer", methods=["GET", "POST"])
def add_customer():
    """
    Allow employees to create new customer accounts.
    
    Returns:
        Redirect to employee dashboard on success or add customer page with errors
    """
    if "emp_id" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        balance_str = request.form.get("balance", "0")
        password = request.form.get("password", "")
        
        conn = None
        try:
            # Validate inputs
            if not full_name:
                raise ValueError("Full name is required")
            if not username:
                raise ValueError("Username is required")
            # Email is optional now
            if not password:
                raise ValueError("Password is required")
                
            validate_username(username)
            if email:
                validate_email(email)
            validate_password(password)
            
            # Validate balance
            try:
                balance = Decimal(str(balance_str))
                if balance < 0:
                    raise ValueError("Initial balance cannot be negative")
            except (InvalidOperation, ValueError):
                raise ValueError("Invalid balance amount")
            
            hashed_password = generate_password_hash(password)
            
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO users (username, password, full_name, email, balance) VALUES (?,?,?,?,?)",
                (username, hashed_password, full_name, email, float(balance))
            )
            conn.commit()
            flash(f"Customer '{username}' added successfully!", "success")
            return redirect(url_for("employee_dashboard"))
            
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("add_customer.html")
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
            return render_template("add_customer.html")
        except Exception as e:
            flash("An error occurred while adding customer. Please try again.", "danger")
            print(f"Add customer error: {str(e)}")
            return render_template("add_customer.html")
        finally:
            if conn:
                conn.close()
                
    return render_template("add_customer.html")

@app.route("/employee/transaction", methods=["GET", "POST"])
def transaction():
    """
    Handle deposits and withdrawals by employees.
    
    Returns:
        Redirect to employee dashboard on success or transaction page with errors
    """
    if "emp_id" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        amount_str = request.form.get("amount", "")
        action_type = request.form.get("action_type", "")  # "Deposit" or "Withdraw"
        
        conn = None
        try:
            # Validate inputs
            if not username:
                raise ValueError("Customer username is required")
            if action_type not in ["Deposit", "Withdraw"]:
                raise ValueError("Invalid transaction type")
                
            amount = validate_amount(amount_str)
            
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, balance FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if not user:
                flash("Customer not found!", "danger")
                return redirect(url_for("transaction", action=action_type))
            
            user_id = user[0]
            balance = Decimal(str(user[1]))
            
            if action_type == "Withdraw" and amount > balance:
                flash(f"Insufficient balance! Customer balance: ${balance:.2f}", "danger")
                return redirect(url_for("transaction", action=action_type))
            
            new_balance = balance + amount if action_type == "Deposit" else balance - amount
            
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (float(new_balance), user_id))
            cursor.execute(
                "INSERT INTO transactions (user_id, emp_id, trans_type, amount, trans_date) VALUES (?,?,?,?,?)",
                (user_id, session["emp_id"], action_type, float(amount), get_egypt_time())
            )
            conn.commit()
            flash(f"{action_type} of ${amount:.2f} successful for {username}!", "success")
            return redirect(url_for("employee_dashboard"))
            
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("transaction", action=action_type))
        except Exception as e:
            if conn:
                conn.rollback()
            flash("An error occurred during transaction. Please try again.", "danger")
            print(f"Transaction error: {str(e)}")
            return redirect(url_for("transaction", action=action_type))
        finally:
            if conn:
                conn.close()
                
    # GET request - show transaction form
    action_type = request.args.get("action", "Deposit")
    return render_template("transaction.html", action_type=action_type)

@app.route("/employee/transfer", methods=["GET", "POST"])
def employee_transfer():
    """
    Handle fund transfers between customer accounts by employees.
    
    Returns:
        Redirect to employee dashboard on success or transfer page with errors
    """
    if "emp_id" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        sender_username = request.form.get("sender_username", "").strip()
        recipient_username = request.form.get("recipient_username", "").strip()
        amount_str = request.form.get("amount", "")
        
        conn = None
        try:
            # Validate inputs
            if not sender_username:
                raise ValueError("Sender username is required")
            if not recipient_username:
                raise ValueError("Recipient username is required")
            if sender_username == recipient_username:
                raise ValueError("Cannot transfer to the same account")
                
            amount = validate_amount(amount_str)
            
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, balance FROM users WHERE username=?", (sender_username,))
            sender = cursor.fetchone()
            cursor.execute("SELECT user_id, balance FROM users WHERE username=?", (recipient_username,))
            receiver = cursor.fetchone()
            
            if not sender:
                flash("Sender account not found!", "danger")
                return redirect(url_for("employee_transfer"))
            if not receiver:
                flash("Recipient account not found!", "danger")
                return redirect(url_for("employee_transfer"))
                
            sender_balance = Decimal(str(sender[1]))
            receiver_balance = Decimal(str(receiver[1]))
            
            if amount > sender_balance:
                flash(f"Insufficient balance! Sender balance: ${sender_balance:.2f}", "danger")
                return redirect(url_for("employee_transfer"))
            
            # Perform transfer
            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount
            
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", 
                         (float(new_sender_balance), sender[0]))
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", 
                         (float(new_receiver_balance), receiver[0]))
            
            # Record transactions
            egypt_now = get_egypt_time()
            cursor.execute(
                "INSERT INTO transactions (user_id, emp_id, trans_type, amount, trans_date) VALUES (?,?,'Transfer Out',?,?)",
                (sender[0], session["emp_id"], float(amount), egypt_now)
            )
            cursor.execute(
                "INSERT INTO transactions (user_id, emp_id, trans_type, amount, trans_date) VALUES (?,?,'Transfer In',?,?)",
                (receiver[0], session["emp_id"], float(amount), egypt_now)
            )
            
            conn.commit()
            flash(f"Transfer successful! ${amount:.2f} from {sender_username} to {recipient_username}", "success")
            return redirect(url_for("employee_dashboard"))
            
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("employee_transfer"))
        except Exception as e:
            if conn:
                conn.rollback()
            flash("An error occurred during transfer. Please try again.", "danger")
            print(f"Employee transfer error: {str(e)}")
            return redirect(url_for("employee_transfer"))
        finally:
            if conn:
                conn.close()
                
    return render_template("employee_transfer.html")

@app.route("/employee/search_customer", methods=["GET", "POST"])
def search_customer():
    if "emp_id" not in session:
        return redirect(url_for("login"))
    customer = None
    transactions = None
    if request.method == "POST":
        search_term = request.form["search_term"]
        conn = get_db()
        cursor = conn.cursor()
        try:
            # Try to search by user_id (integer)
            user_id = int(search_term)
            cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        except ValueError:
            # Search by username (string)
            cursor.execute("SELECT * FROM users WHERE username=?", (search_term,))
        customer = cursor.fetchone()
        if customer:
            cursor.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY trans_date DESC", (customer[0],))
            transactions = cursor.fetchall()
        conn.close()
        if not customer:
            flash("Customer not found!")
    return render_template("search_customer.html", customer=customer, transactions=transactions)


@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE admin_id=?", (session["admin_id"],))
        admin = cursor.fetchone()
        conn.close()
        return render_template("admin_dashboard.html", admin=admin)
    return redirect(url_for("login"))

@app.route("/admin/manage_employees", methods=["GET", "POST"])
def manage_employees():
    if "admin_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            username = request.form["username"]
            password = generate_password_hash(request.form["password"])
            full_name = request.form["full_name"]
            role = request.form["role"]
            try:
                cursor.execute("INSERT INTO employees (username, password, full_name, role) VALUES (?,?,?,?)",
                             (username, password, full_name, role))
                conn.commit()
                flash("Employee added successfully!")
            except sqlite3.IntegrityError:
                flash("Username already exists!")
        elif action == "edit":
            emp_id = request.form["emp_id"]
            full_name = request.form["full_name"]
            role = request.form["role"]
            if request.form.get("password"):
                password = generate_password_hash(request.form["password"])
                cursor.execute("UPDATE employees SET full_name=?, role=?, password=? WHERE emp_id=?",
                             (full_name, role, password, emp_id))
            else:
                cursor.execute("UPDATE employees SET full_name=?, role=? WHERE emp_id=?",
                             (full_name, role, emp_id))
            conn.commit()
            flash("Employee updated successfully!")
        elif action == "delete":
            emp_id = request.form["emp_id"]
            cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
            conn.commit()
            flash("Employee deleted successfully!")
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template("manage_employees.html", employees=employees)

@app.route("/admin/reports")
def reports():
    if "admin_id" not in session:
        return redirect(url_for("login"))
    report_type = request.args.get("type", "transactions")
    conn = get_db()
    cursor = conn.cursor()
    
    if report_type == "transactions":
        cursor.execute("""
            SELECT t.*, u.username as user_name, e.username as emp_name 
            FROM transactions t 
            LEFT JOIN users u ON t.user_id = u.user_id 
            LEFT JOIN employees e ON t.emp_id = e.emp_id 
            ORDER BY t.trans_date DESC
        """)
        data = cursor.fetchall()
    elif report_type == "users":
        cursor.execute("SELECT * FROM users ORDER BY user_id")
        data = cursor.fetchall()
    elif report_type == "employees":
        cursor.execute("SELECT * FROM employees ORDER BY emp_id")
        data = cursor.fetchall()
    else:
        data = []
    
    conn.close()
    return render_template("reports.html", report_type=report_type, data=data)

@app.route("/admin/view_transactions")
def view_transactions():
    if "admin_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.*, u.username as user_name, u.full_name as user_full_name, 
               e.username as emp_name, e.full_name as emp_full_name 
        FROM transactions t 
        LEFT JOIN users u ON t.user_id = u.user_id 
        LEFT JOIN employees e ON t.emp_id = e.emp_id 
        ORDER BY t.trans_date DESC
    """)
    transactions = cursor.fetchall()
    conn.close()
    return render_template("view_transactions.html", transactions=transactions)

# ---------------------------
# Logout
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
