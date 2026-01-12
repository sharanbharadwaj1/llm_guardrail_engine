# LLM Guardrail Engine

A **production-grade guardrail system** for Large Language Models that enforces schema validation, failure-aware retries, confidence scoring, escalation policies, and batch-safe execution.

Designed to treat LLMs as **unreliable components** and ensure deterministic, observable outcomes.

---

## ✨ Key Capabilities

- Schema-first LLM output validation (Pydantic)
- Failure taxonomy (INVALID_JSON, SCHEMA_VIOLATION, REPAIR_EXHAUSTED, LLM_AUTH_FAILURE, etc.)
- Adaptive retry & repair prompts
- Confidence scoring based on retries and failures
- FAST → STRONG model escalation policy
- Batch-safe execution with per-item isolation
- Full observability via run artifacts
- Clean FastAPI interface (single + batch)

---

## 🧱 Tech Stack

- **Python 3.11**
- **FastAPI**
- **Pydantic v2**
- **Groq SDK (OpenAI-compatible API)**
- **Uvicorn**
- **Structured logging**
- **JSON artifact storage**

---

## 📂 Project Structure

guardrails/
├── core/ # REST API endpoints
│ ├── single.py
│ └── batch.py
│
├── core/ # Guardrail engine
│ ├── executor.py # LLM boundary
│ ├── validator.py # Output validation
│ ├── repair.py # Retry + repair logic
│ ├── confidence.py # Confidence scoring
│ ├── precheck.py # Input guardrails
│ ├── observability.py # Run artifacts
│
├── schemas/ # Output schemas
│ ├── summary.py
│ └── batch.py
│
├── prompts/
│ └── summary.txt
│
├── engine.py # Orchestration logic
├── server.py # FastAPI app
├── run.py # Local runner
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🚀 Local Setup (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/llm_guardrail_engine.git
cd llm_guardrail_engine
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv llmg
llmg\Scripts\activate    # Windows
# source llmg/bin/activate  # Linux/Mac
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Set Environment Variables
Create a .env file (do NOT commit this):

ini
Copy code
GROQ_API_KEY=your_groq_api_key_here
Or set manually:

bash
Copy code
setx GROQ_API_KEY "your_groq_api_key_here"
Restart the terminal after setting the variable.

5️⃣ Run the API Server
bash
Copy code
uvicorn app:app --reload
Server will start at:

cpp
Copy code
http://127.0.0.1:8000
🧪 Test the Single Endpoint
PowerShell (Windows)
powershell
Copy code
curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "India announced new regulatory changes affecting digital platforms."
  }'
🧪 Test the Batch Endpoint
powershell
Copy code
curl.exe -X POST http://127.0.0.1:8000/generate-summary/batch `
  -H "Content-Type: application/json" `
  -d '[
    {
      "id": "doc-1",
      "text": "India announced regulatory changes today."
    },
    {
      "id": "doc-2",
      "text": "Hi"
    }
  ]'