-- database/bank_db.sql

CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

-- Users (bank customers)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0.0
);

-- Employees (bank staff)
CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(50)
);

-- Admins
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100)
);

-- Accounts (linked to users)
CREATE TABLE accounts (
    acc_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    acc_type VARCHAR(50),
    balance DECIMAL(10,2) DEFAULT 0.0,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- Transactions
CREATE TABLE transactions (
    trans_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    emp_id INT,
    trans_type VARCHAR(50),
    amount DECIMAL(10,2),
    trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
);
