
---

# ⚡ RAG-Powered Support Bot – Instant Answer Sources

A **RAG-powered support bot** can cut down wait times by pulling instant answers from:

* 📘 **Product Manuals**
  (e.g., PDFs converted into embeddings for setup guides, troubleshooting, and specs)

* 📑 **Policy Documents**
  (returns, refunds, warranties, delivery timelines, replacement terms)

* 🕑 **Past Resolved Queries (`qa_history`)**
  (previous customer queries + accepted solutions to avoid repeated effort)

* 👤 **Customer-Specific Info (`user_kb`)**
  (orders, preferences, warranty status, past issues, delivery status)

---

# ⚙️ Tech Stack

### **Core**

* **Language** → Python 3.10+
* **Framework** → FastAPI (backend API service)
* **Package Management** → `pip`

### **LLM + Embeddings**

* **Embedding Model** → `text-embedding-3-small` (OpenAI)
* **LLM for Answering** → `gpt-4o-mini` (OpenAI)

### **Vector Database**

* **Supabase** → for storing embeddings & performing similarity search via Postgres RBC (stored functions)
* **Client Library** → `supabase-py`

### **Other Dependencies**

* `openai` → for embeddings + completions
* `python-dotenv` → for managing API keys/configs
* `uvicorn` → ASGI server to run FastAPI
* `pydantic` → request/response validation in FastAPI

---

# Database Schema (Supabase)

We’ll keep **3 collections**:

---

### **1. product\_kb**

Holds product-level knowledge.

* `id` → **primary key** (auto)
* `product_id` → **INT** 
* `embedding` → `FLOAT_VECTOR`
* `text` → string

---

### **2. user\_kb**

Holds user-specific knowledge.

* `id` → **primary key** (auto)
* `user_id` → **INT** 
* `embedding` → `FLOAT_VECTOR`
* `text` → string

---

### **3. qa\_history**

Holds **only accepted queries** linked to a product.

* `id` → **primary key** (auto)
* `product_id` → **INT** (foreign key to `product_kb.product_id`)
* `query_text` → string
* `query_embedding` → `FLOAT_VECTOR`
* `solution_text` → string
* `created_at` → datetime


---

# Complete Workflow

1. **User Query**

   * Input: `query + user_id + product_id`
   * Embed query (`text-embedding-3-small`).

2. **Search**

   * Search **product\_kb** (filter by `candidate=product_id`).
   * Search **user\_kb** (filter by `candidate=user_id`).
   * Search **qa\_history** (filter by `product_id`).

3. **Context Assembly**

   * Merge top-k results from all 3 searches.

4. **Answer Generation**

   * Pass `(query + context)` → `gpt-4o-mini`.
   * Return answer to API caller.

5. **Feedback **

   * If the user tags the answer as **“working”**:

     1. Fetch the `solution_text` from `qa_history` at the given `qa_history_id`.
     2. Embed the **new solution text** and **stored solution**(`text-embedding-3-small`).
     3. Compute similarity between the **stored solution embedding** and the **new solution embedding**.
     4. If similarity ≥ threshold:

        * ✅ Consider it redundant → **do not add** to `qa_history`.
     5. Else:

        * ➕ Insert a new record into `qa_history`:

          * `product_id`, `query_text`, `query_embedding`, `solution_text`, `created_at`.
   * If tagged as “not working” → discard.

---

# FastAPI Endpoints

### **POST /query**

```json
{
  "query": "How do I reset my password?",
  "user_id": 42,
  "product_id": 1001
}
```

**Output**

```json
{
  "answer": "You can reset your password by visiting ...",
  "sources": {
    "product_kb":id,
    "user_kb":id,
    "qa_history":id,
  }
}
```

---

### **POST /feedback**

```json
{
  "query": "How do I reset my password?",
  "qa_history":id,
  "solution": "Visit settings → security → reset password",
  "product_id": 1001,
  "user_id": 42
}
```

**Output**

```json
{
  "message": "Feedback saved into qa_history"
  "qa_history_id":id,
}
```

---


# 📂 Project Folder Structure

```bash
rag-customers/
│── .env                        # API keys & configs (OpenAI, Supabase)
│── requirements.txt            # Python dependencies
│── README.md                   # Documentation
│── main.py                     # FastAPI entry point
│
├── app/
│   ├── __init__.py
│   ├── config.py               # Load env variables, Supabase client setup
│   ├── models/                 
│   │   ├── schemas.py          # Pydantic request/response models
│   │   ├── supabase_schema.sql # SQL for Supabase table setup
│   │
│   ├── services/               
│   │   ├── embeddings.py       # Wrapper for OpenAI embeddings
│   │   ├── llm.py              # Wrapper for GPT-4o-mini answering
│   │   ├── search.py           # Supabase similarity search functions (RPC calls)
│   │   ├── feedback.py         # Logic for saving + deduplication in qa_history
│   │
│   ├── routes/                 
│   │   ├── query.py            # /query endpoint
│   │   ├── feedback.py         # /feedback endpoint
│   │   ├── health.py           # /health endpoint (for debugging)
│   │
│   └── utils/                  
│       ├── logger.py           # Logging setup
│       ├── similarity.py       # Cosine similarity + thresholding
│
├── tests/                      
│   ├── __init__.py
│   ├── test_query.py           # Unit tests for query flow
│   ├── test_feedback.py        # Unit tests for feedback flow
│   ├── test_search.py          # Unit tests for Supabase similarity search
│
└── scripts/                    
    ├── init_db.py              # Create Supabase tables + indexes
    ├── seed_data.py            # Load sample product_kb, user_kb, qa_history
```

---

# 📑 File Responsibilities

### **Root**

* `.env` → OpenAI & Supabase keys, DB URLs.
* `requirements.txt` → dependencies (`fastapi`, `uvicorn`, `openai`, `supabase-py`, `pydantic`, `python-dotenv`).
* `main.py` → FastAPI app instance, include routes.

---

### **app/config.py**

* Reads `.env`
* Creates **Supabase client**
* Configures OpenAI client

---

### **app/models/schemas.py**

* Pydantic models for input/output:

  * `QueryRequest`, `QueryResponse`
  * `FeedbackRequest`, `FeedbackResponse`

---

### **app/services/**

* `embeddings.py` → calls OpenAI `text-embedding-3-small`.
* `llm.py` → calls `gpt-4o-mini`.
* `search.py` → Supabase RPC for similarity search.
* `feedback.py` → logic for deduplication + inserting into `qa_history`.

---

### **app/routes/**

* `query.py` → `/query` endpoint (search → context → LLM → return answer).
* `feedback.py` → `/feedback` endpoint (save if unique).
* `health.py` → `/health` for monitoring.

---

### **app/utils/**

* `logger.py` → custom logger for tracking requests/errors.
* `similarity.py` → cosine similarity, thresholding logic.

---

### **tests/**

* `test_query.py` → tests `/query` with sample embeddings.
* `test_feedback.py` → tests deduplication logic.
* `test_search.py` → tests Supabase vector search.

---

### **scripts/**

* `init_db.py` → sets up Supabase schema (`product_kb`, `user_kb`, `qa_history`).
* `seed_data.py` → load sample JSON data for testing.

---

