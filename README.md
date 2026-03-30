# 🌐 Website (Frontend)

This is the **user interface** for the AI Handwriting Recognition System.

## 📁 Files
- `index.html` - Main webpage structure
- `style.css` - Styling and design
- `script.js` - JavaScript logic & API connection

## 🚀 How to Run

### Option 1: Simple HTTP Server
```bash
cd website
python -m http.server 3000
```
Open: `http://localhost:3000`

### Option 2: Live Server (VS Code)
1. Install "Live Server" extension
2. Right-click `index.html`
3. Click "Open with Live Server"

## 🔗 Connection to AI Tool
- Default API URL: `http://127.0.0.1:8000`
- Change in `script.js` → `API_CONFIG.BASE_URL`

## ⚠️ Requirements
- AI Tool backend must be running
- Internet connection (for AWS S3 & OpenAI)
