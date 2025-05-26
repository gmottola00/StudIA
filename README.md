# 📚 StudIA

**StudIA** è una piattaforma AI per studenti e lavoratori universitari.  
Carichi le **slide** o un **PDF**, e il sistema genera automaticamente:

- ✅ Riassunto
- ✅ Flashcard (formato Anki)
- ✅ Quiz con risposte commentate
- ✅ Mappa mentale
- ✅ Audio-lezione

---

## 🧱 Struttura del progetto

```
StudIA/
├── frontend/      # Angular app (interfaccia utente)
├── backend/       # FastAPI + AI services (riassunti, quiz, TTS...)
└── README.md
```

---

## ⚙️ Requisiti

### Per il frontend (Angular):
- Node.js >= 18
- npm
- Angular CLI (`@angular/cli`)

### Per il backend (FastAPI):
- Python >= 3.10
- Poetry (gestione ambienti Python)

---

## 🚀 Setup completo (Linux/Windows)

### 1. Clona il progetto

```bash
git clone https://github.com/gmottola00/StudIA.git
cd StudIA
```

---

### 2. 🔧 Backend – FastAPI con Poetry

```bash
cd backend
poetry install           # Installa le dipendenze
poetry shell             # Entra nell'ambiente virtuale
uvicorn app.main:app --reload
```

📄 Crea un file `.env` nella cartella `backend/`:

```
SUPABASE_URL=...
SUPABASE_KEY=...
OPENAI_API_KEY=...
```

---

### 3. 🌐 Frontend – Angular

```bash
cd frontend
npm install
ng serve
```

➡️ Il frontend sarà disponibile su: `http://localhost:4200`  
➡️ Il backend sarà su: `http://localhost:8000`

---

## 🔐 .env file (esempio)

`backend/.env`
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your_key_here
OPENAI_API_KEY=sk-...
```

---

## 📝 Comandi utili

| Funzione              | Comando                                   |
|-----------------------|-------------------------------------------|
| Avvia backend         | `poetry shell && uvicorn app.main:app --reload` |
| Avvia frontend        | `cd frontend && ng serve`                 |
| Esporta dipendenze    | `poetry export -f requirements.txt --output requirements.txt --without-hashes` |
| Installa Angular CLI  | `npm install -g @angular/cli`            |
| Installa Node con nvm | `nvm install 18 && nvm use 18`            |

---

## 📦 Struttura consigliata backend

```
backend/app/
├── main.py            # Entry point FastAPI
├── routes/            # Endpoint REST (es. /upload, /summary)
├── models/            # Pydantic models
├── services/          # Logica AI, Supabase, TTS
├── utils/             # Funzioni comuni
```

---

## 🛠️ To-do (MVP)

- [x] Setup Angular + FastAPI
- [ ] Upload file e parsing
- [ ] Generazione AI (riassunto, quiz, flashcard)
- [ ] Output PDF + audio TTS
- [ ] Dashboard utente con cronologia studio
