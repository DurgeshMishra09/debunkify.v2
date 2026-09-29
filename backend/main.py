import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .schemas import VerifyRequest
from .services.verifier import verify_content
from .services.image_service import analyze_uploaded_image

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

app = FastAPI(title="DEBUNKIFY API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
def index():
    return FileResponse(INDEX_FILE, headers={"Cache-Control": "no-cache"})

@app.api_route("/health", methods=["GET", "HEAD"], include_in_schema=False)
def health():
    return {
        "success": True,
        "status": "running",
        "serpapi_configured": bool(os.getenv("SERPAPI_KEY")),
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "cloudinary_configured": all(os.getenv(k) for k in (
            "CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET"
        )),
    }

@app.post("/verify")
def verify(request: VerifyRequest):
    if request.type != "news":
        raise HTTPException(status_code=400, detail="Only text/news verification is enabled.")
    if not request.input.strip():
        raise HTTPException(status_code=400, detail="Text is required.")
    if len(request.input) > 5000:
        raise HTTPException(status_code=400, detail="Text is too long. Maximum is 5000 characters.")
    try:
        return verify_content(request)
    except Exception as e:
        print("Verify Error:", e)
        raise HTTPException(status_code=500, detail=f"Verification failed: {e}")

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # matches the "Max 10MB" shown in the UI

# Plain "def" (not "async def"): the analysis makes slow blocking network calls,
# so FastAPI must run it in a worker thread instead of freezing the whole server.
@app.post("/verify/reverse-image")
@app.post("/verify-image")
def reverse_image(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and WEBP images are supported.")
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image is too large. Maximum size is 10MB.")
    return analyze_uploaded_image(file)
