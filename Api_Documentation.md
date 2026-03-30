# 🔗 API Connection Documentation

## Overview
This document explains how the **Website** connects to the **AI Tool**.

## Connection Flow
```
Website (Port 3000) → HTTP Requests → AI Tool (Port 8000) → AWS S3 + OpenAI
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Check connection |
| `/signup` | POST | No | Register user |
| `/login` | POST | No | Get JWT token |
| `/analyze-batch/` | POST | Yes | Process 10 images |

## Authentication Flow
1. User signs up/logs in on Website
2. Website sends credentials to AI Tool
3. AI Tool returns JWT token
4. Website stores token in localStorage
5. All subsequent requests include token in header

## Request Example
```javascript
fetch("http://127.0.0.1:8000/analyze-batch/", {
    method: "POST",
    headers: {
        "Authorization": "Bearer YOUR_TOKEN"
    },
    body: formData
})
```

## Response Example
```json
{
    "status": "success",
    "batch_id": 1,
    "llm_consolidated_analysis": "Summary text...",
    "results": [...]
}
```

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Connection refused | Start AI Tool backend |
| 401 Unauthorized | Check JWT token |
| CORS error | Check CORS settings in main.py |
| 400 Bad Request | Ensure exactly 10 files |
