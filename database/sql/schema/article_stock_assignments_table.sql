CREATE TABLE IF NOT EXISTS stockplatform.article_stock_assignments(
    assignment_id SERIAL PRIMARY KEY,
    stock_id BIGINT,
    article_id BIGINT,
    FOREIGN KEY (stock_id) REFERENCES stockplatform.stocks(stock_id),
    FOREIGN KEY (article_id) REFERENCES stockplatform.articles(article_id)
);