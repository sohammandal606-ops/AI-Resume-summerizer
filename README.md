# 🎬 AI Video & Meeting Summarizer

An end-to-end intelligent video and meeting intelligence platform powered by **Streamlit**, **OpenAI Whisper**, **Sarvam AI**, **Mistral AI**, and **LangChain + ChromaDB RAG**.

Convert YouTube links or uploaded audio/video files into formatted meeting summaries, actionable task lists, key decisions, and an interactive Q&A assistant for deep conversation querying.

---

## 🌟 Key Features

- **📥 Multi-Format Ingestion**:
  - Direct **YouTube URL** processing via `yt-dlp`
  - Local **Audio/Video file uploads** (`.mp4`, `.mp3`, `.wav`, `.m4a`, `.webm`, `.ogg`, `.flac`)
- **🎙️ Dual Transcription Pipeline**:
  - **Local Whisper STT**: Privacy-first offline transcription using OpenAI Whisper (`tiny`, `base`, `small`, `medium`, `large`).
  - **Sarvam AI STT & Translation**: High-accuracy cloud transcription and translation optimized for Indic languages and fast processing.
  - Automatic audio chunking with `pydub` and `static-ffmpeg`.
- **🧠 Intelligent Meeting Synthesis (Mistral AI)**:
  - **Comprehensive Meeting Summaries**: Map-Reduce architecture for handling both short and long meeting transcripts.
  - **Automatic Title Generation**: Context-aware meeting naming.
  - **Action Items Extraction**: Identifies deliverables, owners, and deadlines.
  - **Key Decisions**: Pinpoints consensus and major outcomes.
  - **Open Questions**: Flags unresolved topics for follow-up.
- **💬 Transcript RAG & Interactive Q&A**:
  - Built-in Vector Database with **ChromaDB** and HuggingFace Embeddings (`all-MiniLM-L6-v2`).
  - Chat with the meeting transcript using LangChain LCEL RAG chains to retrieve exact timestamps, quotes, and context.
- **📄 Export & Reports**:
  - Download formatted **PDF** executive summary reports (`ReportLab` / `fpdf2`).
  - Export full transcripts and key takeaways as plain text (`.txt`).
- **✨ Cyber Dark Glassmorphism UI**:
  - Built on Streamlit with custom CSS typography (`Syne` + `JetBrains Mono`), responsive metric cards, and collapsible panels.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    A[YouTube URL / Uploaded Video/Audio] --> B[Audio Processing & Chunking (pydub + ffmpeg)]
    B --> C{Transcription Engine}
    C -->|Local| D[OpenAI Whisper]
    C -->|Cloud / Indic| E[Sarvam AI STT]
    D --> F[Full Transcript]
    E --> F
    F --> G[Vector Store ChromaDB + HuggingFace]
    F --> H[Summarization & Insights Mistral AI]
    G --> I[Conversational RAG Q&A]
    H --> J[Executive Summary]
    H --> K[Action Items & Decisions]
    H --> L[PDF & TXT Export]
```

---

## 📂 Project Structure

```
Ai-video-Summarizer/
├── app.py                     # Main Streamlit web application
├── main.py                    # CLI / alternate entrypoint
├── pyaudioop.py               # Compatibility patch helper
├── requirements.txt           # Python dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
├── core/
│   ├── transcriber.py         # Whisper & Sarvam AI transcription pipelines
│   ├── summarizer.py          # Map-Reduce & direct meeting summarization
│   ├── extractor.py           # Extraction for tasks, decisions, questions
│   ├── vector_store.py        # ChromaDB setup and embedding retriever
│   └── rag_engine.py          # LangChain RAG chain for Q&A
├── utils/
│   └── audio_processor.py     # yt-dlp downloader, chunking & ffmpeg binding
├── downloades/                # Download cache directory (git-ignored)
└── vector_db/                 # ChromaDB persistent storage (git-ignored)
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10+** (Python 3.10 or 3.11 recommended)
- **Git**

> **Note**: `ffmpeg` is automatically handled on Windows via the bundled `static-ffmpeg` package. On Linux/macOS, install via package manager (`sudo apt install ffmpeg` or `brew install ffmpeg`).

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/ai-video-summarizer.git
cd ai-video-summarizer
```

### 3. Create & Activate Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root by copying `.env.example`:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Edit `.env` with your API credentials:

```env
# ── Mistral AI (Required for summarization and RAG)
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-large-latest

# ── Local Whisper Model (Optional default: small)
WHISPER_MODEL=small

# ── Sarvam AI (Optional for Indic languages and fast STT)
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_STT_MODEL=saaras:v2.5
```

---

## 💻 Running the Application

Launch the Streamlit web dashboard:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend UI** | Streamlit, HTML5, Custom CSS |
| **LLM & Reasoning** | Mistral AI (`mistral-large-latest`) |
| **Orchestration** | LangChain (LCEL) |
| **Speech-to-Text** | OpenAI Whisper, Sarvam AI (`saaras:v2.5`) |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Database** | ChromaDB |
| **Media Processing** | `yt-dlp`, `pydub`, `ffmpeg` / `static-ffmpeg` |
| **Document Export** | ReportLab, FPDF2 |

---

## 🔒 Security & Privacy

- Audio and video files downloaded during sessions are cached locally in `downloades/` and excluded from source control.
- API keys in `.env` are strictly protected and ignored via [.gitignore](file:///.gitignore). Never commit your `.env` file.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
