-- 1) Create database
CREATE DATABASE IF NOT EXISTS project2_db;

-- 2) Use the database
USE project2_db;

-- 3) Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 4) Optional: Create calculator history table
CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    num1 FLOAT,
    num2 FLOAT,
    operation VARCHAR(10),
    result VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
