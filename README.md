# SynapseAI

**An AI study companion that turns your notes into quizzes, flashcards, and plain-language explanations.**

SynapseAI is a full-stack AI tutoring app built during final exam prep. Upload a PDF, slide deck, Word doc, or photo of handwritten notes, and it generates quizzes, flashcards, or summaries — or just explains the topic in the simplest way it can, conversationally, with full chat history saved per user.

---

## What it does

- **Chat-based tutoring** — ask it to explain any topic, and it breaks it down in plain language
- **Quiz generation** — turns uploaded material into a 5-question quiz on demand
- **Flashcard generation** — converts notes into Q/A flashcards for studying
- **Document understanding** — reads and extracts content from PDFs, PPTX, and DOCX files
- **Image understanding** — upload a photo of handwritten notes or a textbook page; it reads it directly
- **Streaming responses** — answers stream in token-by-token instead of appearing all at once
- **User accounts** — sign up / sign in, with chat history saved and restored across sessions

## How it's built

SynapseAI is split into two independent services that talk to each other over HTTP — a common pattern for separating the AI/LLM logic from the chat interface.

```
┌─────────────────────┐         HTTP POST /chat        ┌──────────────────────┐
│   frontend/          │ ──────────────────────────────▶ │   backend/            │
│   Chainlit chat UI   │                                  │   FastAPI service     │
│   + Supabase auth    │ ◀────────────────────────────── │   + OpenAI (GPT-4o-mini)│
│   + chat history     │      streamed text response     │                        │
└─────────────────────┘                                  └──────────────────────┘
```

**Frontend (`frontend/`)**
- [Chainlit](https://chainlit.io) — provides the chat UI, file upload widget, and session management
- [Supabase](https://supabase.com) — handles user authentication (sign up / sign in) and stores chat history in Postgres
- `pypdf`, `python-pptx`, `python-docx` — extract raw text from uploaded PDFs, slide decks, and Word docs before sending it to the backend

**Backend (`backend/`)**
- [FastAPI](https://fastapi.tiangolo.com) — a single `/chat` endpoint that takes a message (plus optional image and conversation history) and streams back a response
- [OpenAI API](https://platform.openai.com) (`gpt-4o-mini`) — the actual model doing the explaining, quiz-writing, and flashcard-making, with a system prompt tuned for STEM tutoring and handling multi-question worksheets in full

**Why two services instead of one?** It mirrors how production AI apps are usually structured — a UI layer and a model-serving layer that can be deployed, scaled, or swapped independently. The frontend never talks to OpenAI directly; everything routes through the backend's `/chat` endpoint.

## Tech stack

| Layer | Tech |
|---|---|
| Chat UI | Chainlit |
| Backend API | FastAPI, Uvicorn |
| LLM | OpenAI GPT-4o-mini (streaming) |
| Auth & database | Supabase (Postgres) |
| Document parsing | pypdf, python-pptx, python-docx |

## Running it locally

This project is not deployed anywhere — it was built as a personal study tool and is meant to be run locally. You'll need:

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A free [Supabase](https://supabase.com) project (for auth + chat history)

### 1. Clone the repo

```bash
git clone https://github.com/zain-the-npc/SynapseAI.git
cd SynapseAI
```

### 2. Set up the backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` (copy `.env.example` and fill it in):

```
OPENAI_API_KEY=your-openai-key-here
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Set up the frontend

In a **new terminal**:

```bash
cd frontend
pip install -r requirements.txt
```

Create a `.env` file inside `frontend/` (copy `.env.example` and fill it in):

```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
API_URL=http://localhost:8000/chat
```

You'll also need a `chat_history` table in your Supabase project with columns: `user_id`, `thread_id`, `role`, `content`, `created_at`.

Run the frontend:

```bash
chainlit run chainlit_app.py -w
```

Open the URL Chainlit prints (usually `http://localhost:8000` for the app, separate from the backend port) and sign up with any email/password to start chatting.

## Project structure

```
SynapseAI/
├── backend/
│   ├── main.py              # FastAPI app, /chat endpoint, OpenAI streaming
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── chainlit_app.py      # Chainlit UI, auth, file parsing, chat history
│   ├── public/              # Static assets (mic icon script, etc.)
│   ├── chainlit.md          # Chainlit welcome screen
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Known limitations

- **No deployment** — built and run locally only, by design
- **CORS is wide open** (`allow_origins=["*"]`) on the backend — fine for local use, would need tightening before any real deployment
- **No automated tests** — this was a focused exam-week build, not a production app
- **Single model** — currently hardcoded to `gpt-4o-mini`; not configurable via environment variable yet

## Why this exists

Built during final exam prep as a way to study smarter — instead of re-reading notes, I could upload them and get a quiz, a set of flashcards, or a plain-language explanation back in seconds. It's a small project, but it covers a full slice of a real AI product: an LLM-backed API, a chat interface, file parsing, auth, and persistent history.
