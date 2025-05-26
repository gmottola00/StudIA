# 🧠 StudIA – Backend

Questo è il backend del progetto **StudIA**, un'applicazione AI-first per supportare studenti universitari nello studio da slide e appunti, basata su FastAPI + Supabase + Milvus.

---

## 🗂️ Struttura delle cartelle

```
backend/
├── app/
│   ├── main.py                      # Entry point FastAPI
│   ├── dependencies.py             # Dependency injection (es. SupabaseService)
│   ├── models/                     # Pydantic models (Course, Document, AIOutput, ecc.)
│   ├── routes/                     # Endpoint REST FastAPI (/documents, /courses, ecc.)
│   ├── services/
│   │   ├── supabase_service.py     # Istanzia tutti i manager per Supabase
│   │   ├── relational_db_manager/  # Manager CRUD per Supabase (Postgres)
│   │   │   ├── document_manager.py
│   │   │   ├── course_manager.py
│   │   │   ├── ai_output_manager.py
│   │   │   └── activity_log_manager.py
│   │   ├── vector_db_manager/      # Integrazione con Milvus per vector search
│   │   │   ├── milvus_connection.py
│   │   │   ├── milvus_collection.py
│   │   │   ├── milvus_database.py
│   │   │   └── embedding.py
│   │   └── pdf_parser/             # Estrazione testo da PDF/slide
│   └── utils/                      # Funzioni comuni riutilizzabili
├── pyproject.toml                  # Configurazione Poetry
├── poetry.lock                     # Lock delle dipendenze
├── .env                            # Variabili ambiente (NON versionato)
└── README.md                       # Questo file
```

---

## ⚙️ Tech stack

- **FastAPI** – Web framework per API asincrone
- **Supabase** – Backend-as-a-Service (PostgreSQL + Auth + Storage)
- **Milvus** – Database vettoriale per Retrieval Augmented Generation (RAG)
- **Poetry** – Gestione ambienti e dipendenze Python
- **Uvicorn** – ASGI server
- **OpenAI / Embedding** – per flashcard, riassunti, quiz, mappe mentali

---

## 🚀 Avvio in locale

Assicurati di avere installato:

- Python 3.10+
- Poetry (`pip install poetry`)
- Milvus (puoi usare Docker o Zilliz Cloud)
- Supabase (cloud o CLI)

### 1. Installa le dipendenze

```bash
cd backend
poetry lock
poetry install
```

### 2. Avvia il backend

```bash
poetry run uvicorn app.main:app --reload
```

### 3. Apri la documentazione

Swagger: http://localhost:8000/docs  
Redoc: http://localhost:8000/redoc

---

## 📌 Variabili d'ambiente (.env)

```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
OPENAI_API_KEY=sk-...
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

---

## 🛠️ Comandi utili

| Comando                        | Descrizione                                |
|-------------------------------|--------------------------------------------|
| `poetry run uvicorn ...`      | Avvia FastAPI                              |
| `poetry install`              | Installa dipendenze                        |
| `poetry shell` / `env activate` | Entra nel venv                            |
| `poetry export`               | Esporta requirements.txt                   |
| `poetry run python -m pytest` | Esegui i test (se presenti)                |

---

## 📘 Moduli principali

| Modulo            | Descrizione                                    |
|-------------------|------------------------------------------------|
| `supabase_service`| Inizializza tutti i manager con Supabase client |
| `document_manager`| Gestione documenti: insert, get, update, delete |
| `ai_output_manager` | Gestione output AI: summary, quiz, ecc.      |
| `vector_db_manager`| Funzioni per Milvus + embedding + RAG         |
| `course_manager`  | Gestione delle materie (es. Calcolo, Fisica…) |
| `pdf_parser`      | Estrazione testo dai file caricati (PDF)       |

---

## 📦 API esposte (routes/)

- `POST /documents` – upload di un documento
- `GET /documents/{id}` – recupero documento
- `POST /ai-outputs` – generazione output AI
- `GET /courses` – lista delle materie dell’utente
- `POST /courses` – creazione di una nuova materia
- (e altri…)

---

## 📄 To-do / espandibilità

- [ ] Endpoint di ricerca semantica via Milvus (RAG)
- [ ] Generazione PDF + audio (TTS)
- [ ] Rate limit / Auth avanzata
- [ ] Integrazione dashboard per cronologia studio

---

Questo backend è pronto per scalare: puoi aggiungere facilmente nuovi manager, parser, fonti AI o API esterne.  
Fammi sapere se vuoi un diagramma visivo dell'architettura o una guida di deploy.
