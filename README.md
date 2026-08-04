# Local AI Course Tutor 

A **100% free, private, and offline AI Course Tutor** that transforms your lecture PDFs and slide decks into an interactive study assistant. 

Unlike generic chatbots, this system relies on a local **Retrieval-Augmented Generation (RAG)** pipeline to answer questions strictly from your uploaded course materials while automatically citing exact page and slide numbers. It also features a built-in evaluation framework to measure retrieval quality (Hit Rate & MRR) and monitor local performance in real-time.

---

**WHAT: Project Definition**
The Local AI Course Tutor is a privacy-first, zero-cost educational assistant designed to ingest course documents (PDF lecture notes, slide decks, syllabi) and transform them into an interactive, course-aligned conversational tutor using a local Retrieval-Augmented Generation (RAG) pipeline.

**WHY: Problem & Motivation**
Eliminate Hallucinations: Prevents broad generic answers by constraining responses strictly to uploaded lecture slides.
100% Free & Local: Eliminates subscription fees, cloud token costs, and API limits.
Complete Privacy: Keeps study notes, university slides, and intellectual property stored locally on disk.
Page-Level Citation: Always tells the student which slide or page number was referenced.

---

## ✨ Features

* **🔒 100% Private & Offline:** Runs entirely on your local machine using Ollama. No API keys, cloud subscriptions, or external data sharing required.
* **⚡ Managed by `uv`:** Lightning-fast environment resolution and package installation.
* **💾 Local SQLite Persistence:** Powered by ChromaDB backed by SQLite (`chroma.sqlite3`). Index your course materials once and query them forever across restarts.
* **📍 Page & Slide Citations:** Every answer cites the exact page or slide number where the information was found.
* **⚡ Blazing Fast Retrieval:** Uses `nomic-embed-text` for semantic vector search and `llama3.2` for instant, streaming answers.
* **📊 Built-in Evaluation Benchmark:** Includes local scripts for synthetic ground-truth generation, Hit Rate/MRR metrics, and LLM-as-a-Judge grading.
* **📈 Telemetry & Monitoring Dashboard:** Tracks search latency, response generation time, prompt lengths, and user satisfaction in real-time.

---

## 🏗️ System Architecture

```text
[ Upload PDF / Slides ]
          │
          ▼
[ Extract Page Text ] (PyMuPDF keeping slide/page numbers)
          │
          ▼
[ Embed via Ollama ] (nomic-embed-text)
          │
          ▼
[ Store in SQLite Vector Index ] (ChromaDB PersistentClient)
          │
  (User asks a question)
          │
          ▼
[ Semantic Query Match ] ──► Retrieve Top 3 Relevant Context Chunks
          │
          ▼
[ Local LLM Response ] ──► (Llama 3.2 via Ollama) Returns Explanation + Slide Citations
          │
          ▼
[ SQLite Telemetry Log ] ──► Tracks Latency, Tokens, and User Feedback in Real-Time

```

---

## 🚀 Quick Start (GitHub Codespaces / Local Setup)

### 1. Install `uv` & Dependencies

Clone the repository and install all virtual environment dependencies using `uv`:

```bash
# Clone repository
git clone [https://github.com/your-username/course-tutor-app.git](https://github.com/your-username/course-tutor-app.git)
cd course-tutor-app

# Sync project virtual environment using uv
uv sync

```

### 2. Start Ollama & Pull Models

Install Ollama and download the local embedding model and LLM:

```bash
# Install Ollama (Linux / Codespaces)
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# Start Ollama service in background
ollama serve > /dev/null 2>&1 &

# Pull models
ollama pull nomic-embed-text
ollama pull llama3.2

```

### 3. Run the Application

Launch the Streamlit app using `uv`:

```bash
uv run streamlit run app.py

```

Open your browser at `http://localhost:8501`.

---

## 🧪 Evaluation & Monitoring Strategy

This repository includes a multi-tiered evaluation and monitoring workflow tailored for local RAG pipelines:

### 1. Ground Truth Benchmark Generation

Generate synthetic exam questions directly from your vector database to build an automated test suite:

```bash
uv run generate_eval_dataset.py

```

### 2. Retrieval Quality Metrics (Hit Rate & MRR)

Evaluate whether `nomic-embed-text` successfully retrieves the target slide chunks in the top 3 results:

```bash
uv run evaluate_retrieval.py

```

* **Hit Rate @ 3:** Measures if the relevant slide chunk is retrieved.
* **Mean Reciprocal Rank (MRR @ 3):** Measures how high the correct slide chunk ranks in the retrieval results.

### 3. LLM-as-a-Judge Evaluation

Evaluate candidate LLM responses against reference answers for faithfulness and semantic accuracy:

```bash
uv run evaluate_judge.py

```

### 4. Real-Time Telemetry & Monitoring

All user queries, latency metrics, and feedback are saved locally to `monitoring.db`. View live metrics in the built-in Streamlit monitoring dashboard.

---

## 📦 Project Structure

```text
├── course_tutor_db/        # Persistent SQLite vector database directory (auto-created)
├── monitoring.db           # SQLite database for performance telemetry & user feedback
├── app.py                  # Main Streamlit chat application
├── generate_eval_dataset.py# Synthetic Q&A ground-truth generator script
├── evaluate_retrieval.py   # Script for Hit Rate @ K & MRR evaluation
├── evaluate_judge.py      # LLM-as-a-Judge semantic accuracy evaluator
├── logger.py               # SQLite telemetry logging helpers
├── pyproject.toml          # uv project dependencies configuration
├── uv.lock                 # Lockfile for reproducible installs
├── requirements.txt        # Exported dependencies for legacy setups
├── README.md               # Project documentation
└── LICENSE                 # Open-source license

```

---

## 🛠️ Tech Stack & Key Decisions

| Component | Technology | Rationale |
| --- | --- | --- |
| **Package Manager** | `uv` | Ultra-fast environment sync and script execution. |
| **Frontend UI** | Streamlit | Rapid prototyping in 100% Python with native chat components. |
| **PDF Extraction** | PyMuPDF (`fitz`) | High-speed text extraction that preserves slide boundaries for exact citations. |
| **Vector Database** | ChromaDB (`sqlite3`) | Persistent vector storage inside local directory (`./course_tutor_db`) without external server setup. |
| **Local LLM & Embeddings** | Ollama (`llama3.2` + `nomic-embed-text`) | Zero-cost, privacy-first inference on consumer hardware. |
| **Telemetry & Metrics** | SQLite + Streamlit Dashboard | Zero-dependency tracking of retrieval latencies and user satisfaction scores. |

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the evaluation metrics or add automated study quiz generators:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```