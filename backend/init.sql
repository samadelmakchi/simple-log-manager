CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    microservice VARCHAR(255),
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message TEXT,
    url VARCHAR(255),
    idu INTEGER
);

INSERT INTO users (username, hashed_password) VALUES (
    'admin',
    '$2b$12$WqDpi5vQH5JhHv8uUuYZlOPbOoe3De4D.NB6AziA7XEjwvjKxr4I6'
);

-- Pass : SMDadmin61