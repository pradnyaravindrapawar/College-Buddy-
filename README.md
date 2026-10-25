# 🎓 CollegeBuddy: B.K.Birla College AI Chatbot

An intelligent, explainable web chatbot that answers student inquiries about **B.K.Birla College of Arts, Science & Commerce, Kalyan (Autonomous)** regarding admissions, programs (Arts, Commerce, Science, Technology), eligibility, fee refund rules, examinations, and placements using **verified college records**. 

Built with **Hybrid Information Retrieval** (TF-IDF + FastEmbed BGE-small ONNX) and an optional grounded Anthropic Claude LLM layer, strictly constrained to zero-hallucination responses.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client["Frontend (React 18 + Vite + Tailwind CSS)"]
        UI["Chat Interface"]
        Chips["Category Filter & Starter Chips"]
        Explain["'How I Answered' Explainability Panel"]
        Feedback["Thumbs Up / Down Rating"]
        Catalog["FAQ Catalog Modal"]
    end

    subgraph Server["Backend (FastAPI + Python 3.11)"]
        Router["FastAPI REST Router"]
        RateLimit["Rate Limiter (30 req/min/IP)"]
        NLP["NLP Preprocessing & Light Stemmer"]
        
        subgraph HybridEngine["Hybrid Retrieval Engine"]
            TFIDF["scikit-learn TF-IDF (0.4x weight)"]
            FastEmbed["FastEmbed BAAI/bge-small-en-v1.5 (0.6x weight)"]
            Fusion["Score Fusion: 0.4*TFIDF + 0.6*Dense"]
            Gate{"Top Score >= 0.35?"}
        end
        
        subgraph LLMLayer["Optional LLM Rephraser"]
            Claude["Anthropic Claude (Grounded Prompt)"]
        end
        
        DB[("SQLite (chat_logs.db)")]
        DataFile[("CSV Source of Truth (data/faqs.csv)")]
        CacheFile[("Embeddings Cache (embeddings.npy)")]
    end

    UI -->|"POST /api/chat"| Router
    Feedback -->|"POST /api/feedback"| Router
    AdminUI -->|"CRUD & Retrain"| Router
    
    Router --> RateLimit --> NLP
    NLP --> HybridEngine
    DataFile -->|"Startup / Retrain"| HybridEngine
    HybridEngine --> CacheFile
    
    Gate -- "Yes (Confident)" --> Claude
    Gate -- "No (Unsure)" --> Fallback["Fallback: 'I'm not sure' + Top 3 Chips"]
    
    Claude -->|"source: 'llm' or 'retrieval'"| Router
    Fallback -->|"source: 'fallback'"| Router
    Router --> DB
    Router -->|"JSON Payload + Scores"| UI
    Router -->|"Matches & Tokens"| Explain
```

---

## ⚡ Tech Stack Summary

| Layer | Technology | Rationale / Benefits |
|---|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons | Sub-second HMR dev server, responsive mobile-first UI, zero bloat, dark/light theme |
| **Backend** | Python 3.11, FastAPI, Uvicorn | Async performance, auto OpenAPI `/docs`, strict Pydantic v2 type validation |
| **Lexical Search** | scikit-learn `TfidfVectorizer` | High-precision exact keyword matching (course codes, fee amounts, dates) |
| **Dense Search** | FastEmbed (`BAAI/bge-small-en-v1.5`) | Compact 384-dim ONNX CPU embeddings. **No PyTorch or sentence-transformers** (<100MB RAM, fits Render 512MB free tier) |
| **LLM (Optional)**| Anthropic Claude (`claude-haiku-5-5`) | Rephrases only top retrieved FAQ context. If omitted, app operates 100% offline and free via direct retrieval |
| **Storage** | `data/faqs.csv` & SQLite `chat_logs.db` | Single source-of-truth CSV with persistent SQLite logging for feedback and gap analysis |

---

## 🚀 Key Features

![CampusGuide AI Interface & How I Answered Panel](docs/screenshots/ui_preview.jpg)

1. **Dual-Index Hybrid Retrieval**:
   $$\text{Hybrid Score} = 0.4 \times \text{TF-IDF Cosine} + 0.6 \times \text{FastEmbed Dense Cosine}$$
2. **"How I Answered" Explainability Drawer**:
   - Inspect preprocessed semantic tokens (lowercased, punctuation stripped, stop-words removed, stemmed).
   - View top 3 candidate FAQs with animated visual score progress bars.
   - Shows decision provenance: `retrieval`, `llm`, or `fallback`.
3. **Confidence Gating & Interactive Suggestions**:
   - If the top hybrid score falls below `0.35`, the chatbot responds: *"I'm not sure about that..."* and renders the top 3 closest related questions as one-click query chips.
4. **Lightweight Multi-Turn Follow-Ups**:
   - If a follow-up query is under 4 words (e.g., *"and curfew?"* after asking about hostel rooms), the bot automatically prepends the previous user turn to preserve context.
5. **Searchable FAQ Catalog Modal**:
   - Students can browse, filter by category, and instantly search all 224 verified FAQs with 1-click prompt injection into the chat.

---

## 📊 Benchmark Evaluation Results

Evaluated on 47 held-out questions (`eval/test_questions.csv`):

| Retrieval Strategy | Top-1 Accuracy (%) | Top-3 Accuracy (%) | MRR | Out-of-Scope Rejection (%) |
|---|:---:|:---:|:---:|:---:|
| **TF-IDF Lexical Baseline** | 46.3% | 100.0% | 0.9878 | **100.0%** |
| **FastEmbed Dense Baseline** | 100.0% | 100.0% | 1.0000 | 0.0% |
| **Hybrid Dual-Index (Ours)** | **100.0%** | **100.0%** | **1.0000** | **83.3%** |

*Run benchmark locally anytime:* `python eval/run_eval.py`  
*Full report:* [`eval/results.md`](eval/results.md)

---

## 🛠️ Local Development & Quick Start

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 2. Backend Setup
```powershell
# In project root
python -m pip install -r backend/requirements.txt

# Run automated tests
python -m pytest backend/tests -v

# Start FastAPI dev server (port 8000)
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

Backend interactive documentation will be live at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```powershell
# Open a new terminal
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🌐 Public Cloud Deployment Guide

### Phase A: Push Code to GitHub
```powershell
git init
git add .
git commit -m "feat: complete college faq chatbot"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/college-faq-chatbot.git
git push -u origin main
```

---

### Phase B: Deploy Backend on Render (Free Web Service)
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Blueprint** (or **Web Service**).
3. Connect your GitHub repository.
4. If using Blueprint, Render automatically detects [`render.yaml`](render.yaml).
5. If creating Web Service manually:
   - **Environment**: Python
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `PYTHONPATH` = `backend`
     - `ADMIN_TOKEN` = `college-admin-supersecret-2026`
     - `SIMILARITY_THRESHOLD` = `0.35`
     - `FRONTEND_ORIGIN` = `http://localhost:5173,https://<YOUR_APP>.vercel.app`
     - `ANTHROPIC_MODEL` = `claude-haiku-5-5`
     - `ANTHROPIC_API_KEY` = *(Optional: leave blank to run free retrieval mode)*
6. Click **Create Web Service**. Note your public URL (e.g., `https://college-faq-backend.onrender.com`).

> ℹ️ **Cold Start Note**: Render's free tier spins down after 15 minutes of inactivity. When a student visits after idle time, the frontend automatically displays: *"Waking up cloud server (takes ~30-50s on initial load)..."*

---

### Phase C: Deploy Frontend on Vercel
1. Log in to [vercel.com](https://vercel.com) and click **Add New...** $\rightarrow$ **Project**.
2. Import your GitHub repository.
3. Configure the build settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL` = `https://<YOUR_RENDER_BACKEND_URL>.onrender.com`
5. Click **Deploy**. Your chatbot will be live on a public `*.vercel.app` URL!

---

### Post-Deployment Verification Checklist
- [ ] **Health Check**: Open `https://<YOUR_RENDER_BACKEND>.onrender.com/api/health` $\rightarrow$ returns `{"status":"ok","faqs_count":20}`.
- [ ] **Chat Query**: Ask *"How much is the B.Tech tuition fee?"* $\rightarrow$ returns verified fee details with source pill and confidence score.
- [ ] **Explainability**: Click *"How I answered"* $\rightarrow$ drawer displays tokens and score breakdown.
- [ ] **Feedback Test**: Click Thumbs Up $\rightarrow$ confirms *"Saved!"* and records to SQLite.
- [ ] **Admin Portal**: Open `/admin`, enter `college-admin-supersecret-2026`, and verify that the dashboard renders metrics and unanswered queries.

---

## 🎓 Oral Examination / Viva Q&A (Top 15 Defense Questions)

### Q1: What is the core difference between TF-IDF and Dense Semantic Embeddings?
**Answer:** TF-IDF (Term Frequency-Inverse Document Frequency) is a sparse lexical model that measures exact word overlap and assigns higher weight to terms rare across documents. Dense Embeddings (like BGE-small) map sentences into a continuous 384-dimensional latent vector space where geometric distance reflects semantic similarity regardless of wording.

### Q2: Why did you choose a Hybrid Retrieval approach instead of only using Embeddings?
**Answer:** In empirical testing (`eval/results.md`), embeddings alone achieved 100% on in-scope questions but had a 0% rejection rate for out-of-scope queries (semantic over-generalization). TF-IDF alone had 100% rejection but only 46.3% Top-1 accuracy due to vocabulary mismatch. The hybrid formula ($0.4 \times \text{TFIDF} + 0.6 \times \text{Dense}$) combines exact lexical grounding with conceptual understanding.

### Q3: What is Cosine Similarity and why is it preferred over Euclidean Distance?
**Answer:** Cosine similarity measures the cosine of the angle between two vectors:
$$\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
It evaluates directional orientation rather than magnitude, ensuring that document length differences do not distort similarity scores.

### Q4: Why did you use FastEmbed with ONNX runtime instead of PyTorch or Sentence-Transformers?
**Answer:** Free cloud tiers (such as Render) have strict memory ceilings of 512 MB RAM. Standard PyTorch + transformers libraries consume 800 MB to 1.5 GB just loading CUDA/C++ bindings. FastEmbed runs quantized ONNX models on CPU consuming under 100 MB RAM, preventing Out-Of-Memory (OOM) crashes.

### Q5: How was the confidence threshold of 0.35 determined?
**Answer:** Through our held-out benchmark evaluation (`eval/run_eval.py`). At 0.35, the system maximized the F1-score: correctly answering 100% of in-scope college questions while rejecting 83.3% of adversarial out-of-scope questions.

### Q6: How does the system prevent LLM hallucinations?
**Answer:** 
1. The LLM is strictly constrained via system prompt instructions to synthesize only retrieved FAQ document snippets.
2. If similarity falls below 0.35, the LLM is bypassed entirely and the fallback message is returned directly.
3. Temperature is set to 0.0 for deterministic factual fidelity.

### Q7: What happens if the Anthropic API key is missing or expires?
**Answer:** The architecture implements graceful degradation. If `ANTHROPIC_API_KEY` is not set or API fails, the backend immediately returns the verified FAQ answer directly with `source: "retrieval"`. The app never crashes.

### Q8: Why did you build an engineered index text ($3 \times \text{Question} + 2 \times \text{Paraphrases} + \dots$)?
**Answer:** In student inquiries, the user's query aligns closest with the problem statement rather than long procedural answers. Repeating the question and paraphrases boosts their term frequency and attention weights in vector space.

### Q9: What preprocessing steps does your NLP pipeline perform?
**Answer:**
1. Lowercasing (normalizes casing variance).
2. Punctuation stripping (removes syntax noise like `?` or `!`).
3. Whitespace tokenization.
4. Stopword filtering (removes non-informative words like *is, the, what*).
5. Suffix-based light stemming (*fees* $\rightarrow$ *fee*, *placements* $\rightarrow$ *placement*).
6. Domain synonym expansion via `data/synonyms.json` (*dorm* $\rightarrow$ *hostel*).

### Q10: How does the system handle multi-turn follow-ups?
**Answer:** If an incoming student query is under 4 words (e.g., *"and timings?"*), the backend looks at the conversation history and prepends the previous user turn (e.g., *"What hostel facilities are provided? and timings?"*), resolving conversational anaphora.

### Q11: How do you handle disk caching of embeddings?
**Answer:** Precomputed dense vectors are saved as `data/embeddings.npy` along with an MD5 hash of the FAQ content. On server startup, the system loads vectors directly from disk in milliseconds instead of re-encoding documents.

### Q12: How does the Admin Zero-Downtime Retraining work?
**Answer:** When an administrator adds, edits, or deletes FAQs, the endpoint re-fits the TF-IDF vectorizer and recomputes embeddings in memory and persists them to disk. The retriever pointer is updated atomically without restarting the process.

### Q13: What security measures protect the API?
**Answer:**
1. In-memory sliding-window rate limiting (30 requests per minute per IP).
2. Input length limits (500-character maximum).
3. Pydantic schema validation preventing malformed payloads.
4. Bearer token authorization on all `/api/admin/*` routes.
5. Strict CORS origins for the frontend domain.

### Q14: What is the purpose of the SQLite `chat_logs.db`?
**Answer:** It records student queries, matched FAQ IDs, confidence scores, and user ratings (Thumbs Up/Down). This powers the Admin dashboard's knowledge gap analysis, identifying frequent unanswered queries so the college can update its policies.

### Q15: What are the current limitations and future scope?
**Answer:**
- *Current limitation*: Keyword-based multi-turn handling is lightweight and does not track multi-depth pronoun resolution.
- *Future scope*: Adding cross-encoder reranking (e.g., BGE-Reranker-small), multilingual queries (Hindi/regional languages), and speech-to-text input.

---

## 📁 Repository Directory Structure

```text
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI endpoints, CORS, rate limiting
│   │   ├── nlp.py           # Tokenization, stemming, synonym mapping
│   │   ├── retriever.py     # Hybrid TF-IDF + FastEmbed engine
│   │   ├── llm.py           # Anthropic Claude grounded integration
│   │   ├── db.py            # SQLite chat logging & feedback metrics
│   │   └── schemas.py       # Pydantic data contracts
│   ├── tests/
│   │   ├── test_nlp.py
│   │   ├── test_retriever.py
│   │   └── test_api.py
│   ├── Dockerfile           # Container definition
│   ├── requirements.txt     # Python dependencies
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, ExplainPanel, MessageItem, StarterChips...
│   │   ├── pages/           # ChatPage, AdminPage
│   │   ├── api.js           # API client
│   │   ├── App.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── data/
│   ├── faqs.csv             # Source of truth FAQ database
│   ├── sample_faqs.csv      # 20 starter college records
│   └── synonyms.json        # Domain synonym dictionary
├── eval/
│   ├── test_questions.csv   # 47 held-out test questions
│   ├── run_eval.py          # Benchmark script
│   └── results.md           # Generated comparative report
├── scripts/
│   ├── validate_data.py     # CSV schema & consistency checker
│   └── generate_csv.py      # Compliant RFC CSV generator
├── render.yaml              # Render deployment blueprint
├── .gitignore
└── README.md
```

---

## 📜 License
Developed as an educational Final-Year Undergraduate Engineering Mini-Project. Open-sourced under the MIT License.
