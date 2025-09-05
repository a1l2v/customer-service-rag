CREATE TABLE product_kb (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    embedding FLOAT8[],
    text TEXT NOT NULL
);

CREATE TABLE user_kb (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    embedding FLOAT8[],
    text TEXT NOT NULL
);

CREATE TABLE qa_history (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product_kb(product_id),
    query_text TEXT NOT NULL,
    query_embedding FLOAT8[],
    solution_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);