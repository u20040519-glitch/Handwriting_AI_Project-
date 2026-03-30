from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from pydantic import BaseModel

from modules.preprocessing import preprocess_image
from modules.ocr_engine import recognize_handwriting
from modules.llm_engine import analyze_batch_text
from modules.cloud_storage import upload_to_cloud
from modules.database import get_db, User, Batch, Record, SessionLocal
from modules.auth import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI(
    title="AI Handwriting Recognition Tool",
    description="Backend AI Tool for handwriting recognition",
    version="1.0.0"
)

# CORS Middleware (Allow Website Connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Auth Routes ---
@app.post("/signup", response_model=Token, tags=["Authentication"])
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# --- Protected Analysis Route ---
@app.post("/analyze-batch/", tags=["AI Processing"])
async def analyze_handwriting_batch(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze 10 handwriting samples (Protected Route)"""

    if len(files) != 10:
        raise HTTPException(status_code=400, detail="Exactly 10 samples are required.")

    # Create batch linked to user
    new_batch = Batch(user_id=current_user.id)
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    results = []
    all_ocr_texts = []

    for index, file in enumerate(files):
        try:
            contents = await file.read()
            file_ext = file.filename.split(".")[-1] if "." in file.filename else "png"

            processed_img = preprocess_image(contents)
            raw_text = recognize_handwriting(processed_img)
            all_ocr_texts.append(f"Sample {index+1}: {raw_text}")

            cloud_url = upload_to_cloud(contents, file_ext)

            if cloud_url:
                record = Record(batch_id=new_batch.id, image_url=cloud_url, ocr_text=raw_text)
                db.add(record)

            results.append({
                "sample_id": index + 1,
                "cloud_url": cloud_url,
                "ocr_text": raw_text
            })

        except Exception as e:
            results.append({
                "sample_id": index + 1,
                "error": str(e),
                "cloud_url": None,
                "ocr_text": None
            })

    db.commit()

    combined_text = "\n".join(all_ocr_texts)
    llm_summary = analyze_batch_text(combined_text)

    return {
        "status": "success",
        "user": current_user.username,
        "batch_id": new_batch.id,
        "samples_processed": len(results),
        "llm_consolidated_analysis": llm_summary,
        "results": results
    }

# --- Health Check ---
@app.get("/", tags=["Health"])
async def root():
    return {"message": "AI Handwriting Recognition Tool is running", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
