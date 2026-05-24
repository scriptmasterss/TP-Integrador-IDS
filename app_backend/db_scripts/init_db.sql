CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    score INT DEFAULT 0,
    role enum('student', 'teacher', 'librarian', 'admin') NOT NULL DEFAULT 'student',
    major VARCHAR(50),
    password_hash VARCHAR(255) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    section VARCHAR(50) NOT NULL,
    max_loan_duration INT NOT NULL,
    stock INT DEFAULT 1,
    needs_repair BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    pickup_date DATETIME NOT NULL,
    return_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS return_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    days_late INT DEFAULT 0,
    conditions VARCHAR(50),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

CREATE TABLE IF NOT EXISTS penalties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reservation_id INT,
    reason VARCHAR(255),
    start_date DATETIME,
    end_date DATETIME,
    active BOOLEAN DEFAULT TRUE,
    severity enum('low', 'medium', 'high') NOT NULL DEFAULT 'medium',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

CREATE TABLE IF NOT EXISTS qr_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT,
    generated_at DATETIME NOT NULL,
    code VARCHAR(255) UNIQUE,
    scanned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

CREATE TABLE IF NOT EXISTS policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    date DATETIME
);
