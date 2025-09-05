# RAG-Powered Support Bot

## Overview

The RAG-Powered Support Bot is designed to provide instant answers to customer queries by leveraging a Retrieval-Augmented Generation (RAG) approach. This bot pulls information from various sources, including product manuals, policy documents, past resolved queries, and customer-specific information, to deliver accurate and timely responses.

## Features

- Instant answers from product manuals and policy documents.
- Utilizes past resolved queries to avoid redundancy.
- Provides customer-specific information for personalized support.
- Built with FastAPI for high performance and scalability.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Machine Learning**: OpenAI's GPT-4o-mini and text-embedding-3-small

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd rag-customers
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Create a `.env` file in the root directory and add your OpenAI and Supabase API keys and database URLs.

5. **Initialize the Database**
   - Run the `init_db.py` script to set up the Supabase schema.
   ```bash
   python scripts/init_db.py
   ```

6. **Seed Sample Data**
   - Optionally, run the `seed_data.py` script to load sample data for testing.
   ```bash
   python scripts/seed_data.py
   ```

7. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- **Query Endpoint**: Send a POST request to `/query` with the user's query, user ID, and product ID to receive an answer.
- **Feedback Endpoint**: Send a POST request to `/feedback` to provide feedback on the answers received.

## Testing

Unit tests are provided in the `tests` directory. You can run the tests using:
```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.