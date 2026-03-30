# 🤖 AI Tool (Backend)

This is the **AI/ML backend** that processes handwriting images.

## 📁 Files
- `main.py` - FastAPI entry point
- `modules/` - AI processing modules
- `.env` - Configuration (API keys)
- `requirements.txt` - Dependencies

## 🚀 How to Run

### 1. Install Dependencies
```bash
cd ai-tool
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` with your AWS & OpenAI keys

### 3. Run Server
```bash
uvicorn main:app --reload
```

### 4. Access API Docs
Open: `http://127.0.0.1:8000/docs`

## 🔗 Connection to Website
- Default Port: `8000`
- CORS enabled for all origins (change for production)
