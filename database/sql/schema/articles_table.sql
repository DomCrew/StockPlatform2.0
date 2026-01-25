DROP TABLE IF EXISTS stockplatform.articles CASCADE;

CREATE TABLE IF NOT EXISTS stockplatform.articles(
    article_id SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    title TEXT UNIQUE NOT NULL,
    summary TEXT,
    link TEXT UNIQUE,
    sa_label VARCHAR(10),
    sa_score FLOAT
);