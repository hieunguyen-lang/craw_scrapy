CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    description TEXT,
    content LONGTEXT,
    author VARCHAR(255),
    published_date DATETIME,
    tags TEXT,
    image_url TEXT,
    url VARCHAR(255),
    UNIQUE KEY unique_url (url)
);