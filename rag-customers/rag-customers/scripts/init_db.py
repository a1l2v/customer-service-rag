import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

def init_db():
    # Load database connection details from environment variables
    db_url = os.getenv("SUPABASE_DB_URL")
    db_user = os.getenv("SUPABASE_DB_USER")
    db_password = os.getenv("SUPABASE_DB_PASSWORD")
    db_name = os.getenv("SUPABASE_DB_NAME")

    # Connect to the Supabase database
    conn = psycopg2.connect(
        host=db_url,
        user=db_user,
        password=db_password,
        dbname=db_name
    )
    
    cursor = conn.cursor()

    # SQL commands to create the necessary tables
    create_product_kb_table = """
    CREATE TABLE IF NOT EXISTS product_kb (
        id SERIAL PRIMARY KEY,
        product_id INT NOT NULL,
        embedding FLOAT8[],
        text TEXT NOT NULL
    );
    """

    create_user_kb_table = """
    CREATE TABLE IF NOT EXISTS user_kb (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        embedding FLOAT8[],
        text TEXT NOT NULL
    );
    """

    create_qa_history_table = """
    CREATE TABLE IF NOT EXISTS qa_history (
        id SERIAL PRIMARY KEY,
        product_id INT REFERENCES product_kb(product_id),
        query_text TEXT NOT NULL,
        query_embedding FLOAT8[],
        solution_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Execute the SQL commands
    cursor.execute(create_product_kb_table)
    cursor.execute(create_user_kb_table)
    cursor.execute(create_qa_history_table)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()