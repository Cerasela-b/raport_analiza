CREATE DATABASE movies_db;
USE movies_db;

CREATE TABLE movies (
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    director VARCHAR(255) NOT NULL,
    language VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    duration INT NOT NULL CHECK (duration > 0),
    budget DECIMAL(15, 2) NOT NULL CHECK (budget >= 0),
    box_office DECIMAL(15, 2) NOT NULL CHECK (box_office >= 0)
);

SELECT genre, SUM(box_office) AS castig_total
FROM movies
GROUP BY genre
ORDER BY castig_total DESC
LIMIT 3;

SELECT 
	AVG(budget) AS buget_mediu,
	AVG(box_office) AS castig_mediu
FROM movies;
