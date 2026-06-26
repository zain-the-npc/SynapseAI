# SynapseAI 🧠

**A multimodal AI study companion — upload a PPT, PDF, Word doc, or a photo of your notes, and it explains, quizzes, or makes flashcards out of it.**

I built this during my final exams because I was tired of re-reading the same notes without retaining anything. SynapseAI reads whatever I throw at it — slides, documents, or handwritten notes — and turns it into something I can actually study from: a quiz, a set of flashcards, or a plain-language explanation, all through chat.

---

## What it does ✨

- 💬 **Chat-based tutoring** — ask it to explain any topic, it breaks it down in the simplest way possible
- 📝 **Quiz generation** — turns uploaded material into a 5-question quiz on demand
- 🗂️ **Flashcard generation** — converts notes into Q/A flashcards for studying
- 📄 **Document understanding** — reads and extracts content from PDFs, PPTX, and DOCX files
- 🖼️ **Image understanding** — upload a photo of handwritten notes or a textbook page; it reads it directly, no manual typing needed
- ⚡ **Streaming responses** — answers stream in token-by-token like a real chat, not a wall of text dropped all at once
- 🔐 **User accounts** — sign up / sign in, with chat history saved and restored across sessions
- 🚀 **Quick-start prompts** — one-tap buttons for "make a quiz," "summarize," or "make flashcards" so you don't have to type the same instructions every time

## How it's built 🏗️

Two services talk to each other: a Chainlit chat UI (frontend) and a FastAPI service (backend) that calls OpenAI's GPT-4o-mini.

**Frontend** — Chainlit for the chat interface, Supabase for auth and chat history, plus `pypdf`/`python-pptx`/`python-docx` to read uploaded files.

**Backend** — A single FastAPI endpoint that takes a message (text, image, or extracted document text) and streams back a response from GPT-4o-mini.

## Tech stack 🛠️

| Layer | Tech |
|---|---|
| Chat UI | Chainlit |
| Backend API | FastAPI, Uvicorn |
| LLM | OpenAI GPT-4o-mini (streaming) |
| Auth & database | Supabase (Postgres) |
| Document parsing | pypdf, python-pptx, python-docx |

## Running it locally 💻

This isn't deployed anywhere — it's meant to run locally. You'll need Python 3.10+, an OpenAI API key, and a Supabase project.

```bash
git clone https://github.com/zain-the-npc/SynapseAI.git
cd SynapseAI

# Backend
cd backend
pip install -r requirements.txt
# create .env with OPENAI_API_KEY=your-key-here
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
pip install -r requirements.txt
# create .env with SUPABASE_URL, SUPABASE_KEY, API_URL=http://localhost:8000/chat
chainlit run chainlit_app.py -w
```

Sign up with any email/password to start chatting.

## Known limitations ⚠️

- **No deployment** — built and run locally only, by design
- **CORS is wide open** (`allow_origins=["*"]`) on the backend — fine for local use, would need tightening before any real deployment
- **No automated tests** — this was a focused exam-week build, not a production app
- **Single model** — currently hardcoded to `gpt-4o-mini`; not configurable via environment variable yet
