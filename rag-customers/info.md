
---

# Database Schema (Milvus)

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

# Updated Workflow

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

5. **Feedback**

   * If user tags answer as “working” → insert into `qa_history`:

     * `product_id`, `query_text`, `query_embedding`, `solution_text`, `created_at`.
   * Otherwise → discard.

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
  "sources": ["product_kb", "qa_history"]
}
```

---

### **POST /feedback**

```json
{
  "query": "How do I reset my password?",
  "solution": "Visit settings → security → reset password",
  "product_id": 1001,
  "user_id": 42
}
```

**Output**

```json
{
  "message": "Feedback saved into qa_history"
}
```

---

