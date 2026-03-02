SHL GenAI Assessment Recommendation Engine
📌 Problem Statement

Build a GenAI-powered web-based system that recommends relevant SHL assessments based on job requirements.

The system should:

Retrieve relevant assessments from SHL’s product catalog

Use semantic search + neural reranking

Return structured results via API

Be evaluated using Mean Recall@10

🏗 System Architecture
User Query
   ↓
Query Enhancement
   ↓
SentenceTransformer (all-MiniLM-L6-v2)
   ↓
FAISS Vector Search (Top 75)
   ↓
Keyword Boosting
   ↓
CrossEncoder Reranking (ms-marco-MiniLM-L-6-v2)
   ↓
Top 10 Assessments
   ↓
FastAPI Backend
   ↓
Streamlit Frontend
🧠 Models Used
🔹 Embedding Model

all-MiniLM-L6-v2
Used to generate dense vector embeddings for assessments and queries.

🔹 Vector Database

FAISS
Efficient similarity search over 500+ SHL assessments.

🔹 Neural Reranker

cross-encoder/ms-marco-MiniLM-L-6-v2
Improves ranking quality using deep semantic matching.

📊 Evaluation

Evaluation Metric: Mean Recall@10

Performance Improvement Journey:
Stage	Recall@10
Embedding-only retrieval	~0.13
Structured document embeddings	~0.27
CrossEncoder reranking	~0.30

Final Model:
Mean Recall@10 ≈ 0.30

🚀 Features

500+ SHL assessments scraped and structured

Two-stage RAG pipeline

Semantic search using FAISS

Neural reranking

Evaluation pipeline

FastAPI REST API

Streamlit interactive UI

Modular project architecture

📂 Project Structure
shl-assessment-recommender/
│
├── api/                     # FastAPI backend
├── retrieval/               # Retrieval logic
├── llm/                     # CrossEncoder reranker
├── embeddings/              # Embedding generation
├── evaluation/              # Recall evaluation
├── frontend/                # Streamlit UI
├── data/                    # Dataset + embeddings
├── requirements.txt
└── README.md
🛠 How to Run Locally
1️⃣ Install Dependencies
pip install -r requirements.txt
2️⃣ Generate Embeddings
python embeddings/generate_embeddings.py
3️⃣ Start Backend
uvicorn api.main:app --reload

API runs at:

http://127.0.0.1:8000/docs
4️⃣ Start Frontend
streamlit run frontend/streamlit_app.py

App runs at:

http://localhost:8501
🔎 Example Query
Looking to hire a Java developer with strong analytical reasoning and collaboration skills. Assessments should be completed within 60 minutes.
🎯 Technical Highlights

Structured document embeddings for better semantic matching

Query enhancement for alignment with document format

Hybrid retrieval (semantic + heuristic boosting)

Neural reranking for improved precision

Evaluation-driven development

📈 Future Improvements

Fine-tuned ranking model

Duration-aware constraint modeling

Deployment (Docker + Cloud)

Advanced UI enhancements

👨‍💻 Author

Sagili Manjunatha Reddy
B.Tech CSE (AIML)
GenAI | NLP | RAG Systems

GitHub: https://github.com/sagilimanjunathareddy
