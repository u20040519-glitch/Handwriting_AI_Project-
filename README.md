# 🖊️ AI Handwriting Recognition System

A complete cloud-native AI system with separated Website, AI Tool, and API Connection.

## 🏗️ Project Structure

```
handwriting_ai_project/
├── website/           # Frontend (User Interface)
├── ai-tool/           # Backend (AI/ML Processing)
├── api-connection/    # Connection Config & Docs
└── README.md          # This file
```

## 🚀 Quick Start

### Step 1: Start AI Tool (Backend)
```bash
cd ai-tool
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Edit .env with your API keys
uvicorn main:app --reload
```

### Step 2: Start Website (Frontend)
```bash
cd website
python -m http.server 3000
```

### Step 3: Test Connection
```bash
cd api-connection
python test_connection.py
```

### Step 4: Open Website
Open: `http://localhost:3000`

## 🔗 Component Communication

```
┌─────────────┐      HTTP/JSON      ┌─────────────┐
│   Website   │ ──────────────────→ │   AI Tool   │
│  (Port 3000)│                     │  (Port 8000)│
└─────────────┘                     └──────┬──────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
              ┌──────────┐          ┌──────────┐          ┌──────────┐
              │ AWS S3   │          │ OpenAI   │          │ SQLite   │
              │ (Storage)│          │  (LLM)   │          │  (DB)    │
              └──────────┘          └──────────┘          └──────────┘
```

## 📋 Features

| Component | Features |
|-----------|----------|
| Website | User Auth, File Upload, Results Display |
| AI Tool | OCR, LLM, Cloud Storage, Database |
| Connection | JWT Auth, REST API, Health Checks |

## 🔐 Security
- JWT Token Authentication
- Password Hashing (bcrypt)
- CORS Configuration
- Environment Variables (.env)

## 🛠️ Technologies

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI, Python |
| AI/ML | TrOCR, OpenCV, PyTorch |
| LLM | OpenAI GPT-3.5 |
| Storage | AWS S3 |
| Database | SQLite |

## 📝 License
MIT License
```

---

## ✅ Complete Setup Checklist

| Component | Task | Status |
|-----------|------|--------|
| **Website** | Create folder | ✅ |
| | Add HTML/CSS/JS | ✅ |
| | Configure API URL | ✅ |
| **AI Tool** | Create folder | ✅ |
| | Install dependencies | ✅ |
| | Configure .env | ✅ |
| | Run server | ✅ |
| **Connection** | Test API | ✅ |
| | Verify CORS | ✅ |
| | Check health endpoint | ✅ |

---

## 🎉 Your Project is Fully Separated!

You now have:
1. **Website** - Runs independently on Port 3000
2. **AI Tool** - Runs independently on Port 8000
3. **API Connection** - Clear documentation & testing

Start both servers and enjoy your complete AI Handwriting Recognition System! 🚀
