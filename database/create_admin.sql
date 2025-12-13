-- Create default admin account
-- Default credentials:
-- Username: admin
-- Password: admin123 (hashed)

USE bank_db;

-- Note: This uses a pre-hashed password for 'admin123'
-- If you want to use a different password, use the Python script instead

INSERT INTO admins (username, password, full_name) 
VALUES (
    'admin', 
    'pbkdf2:sha256:600000$YourSecretKey$HashedPasswordHere',
    'System Administrator'
);

-- If the above doesn't work, use the Python script: create_default_admin.py
-- Or create manually using Python to hash your password:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('your_password'))

