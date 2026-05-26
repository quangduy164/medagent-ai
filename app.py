# app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import numpy as np
from PIL import Image as PILImage
from agents.orchestrator import MedicalAgentOrchestrator
from models.bridge import generate_prompt
from models.decoder import BioGPTDecoder

app = FastAPI(title="AI Medical Vision Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Serve test_samples — phải mount TRƯỚC middleware để CORS áp dụng đúng
TEST_SAMPLES_DIR = "test_samples"
os.makedirs(TEST_SAMPLES_DIR, exist_ok=True)

# Serve ảnh output (heatmap, result)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# Serve React build (nếu đã build)
FRONTEND_BUILD = "frontend/build"
if os.path.exists(FRONTEND_BUILD):
    app.mount("/static", StaticFiles(directory=f"{FRONTEND_BUILD}/static"), name="static")

print("⏳ Starting Server & Loading Multi-Agent System...")
ai_agent  = MedicalAgentOrchestrator()
_decoder  = BioGPTDecoder()


@app.get("/test-samples-static/{category}/{filename}")
async def serve_test_sample(category: str, filename: str):
    """Serve ảnh mẫu với CORS header đúng."""
    file_path = os.path.join(TEST_SAMPLES_DIR, category, filename)
    if not os.path.exists(file_path):
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(file_path)


@app.get("/test-samples")
async def get_test_samples():
    """Trả về danh sách ảnh mẫu theo category."""
    result = {}
    if not os.path.exists(TEST_SAMPLES_DIR):
        return JSONResponse(result)
    for category in sorted(os.listdir(TEST_SAMPLES_DIR)):
        cat_path = os.path.join(TEST_SAMPLES_DIR, category)
        if not os.path.isdir(cat_path):
            continue
        images = [
            f"/test-samples-static/{category}/{fname}"
            for fname in sorted(os.listdir(cat_path))
            if fname.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        if images:
            result[category] = images
    return JSONResponse(result)


@app.get("/")
async def serve_frontend():
    index = f"{FRONTEND_BUILD}/index.html"
    if os.path.exists(index):
        return FileResponse(index)
    return {"message": "API is running. Frontend not built yet."}


def is_xray_image(path: str) -> bool:
    """Kiểm tra ảnh có phải X-quang không dựa trên HSL saturation."""
    try:
        img = PILImage.open(path).convert("RGB").resize((200, 200))
        arr = np.array(img, dtype=np.float32) / 255.0
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        max_c = np.max(arr, axis=2)
        min_c = np.min(arr, axis=2)
        lightness = (max_c + min_c) / 2
        diff = max_c - min_c
        # Saturation theo HSL
        sat = np.where(
            diff == 0, 0,
            np.where(lightness < 0.5,
                     diff / (max_c + min_c + 1e-8),
                     diff / (2 - max_c - min_c + 1e-8))
        )
        # Pixel có màu rõ: sat > 15% và không quá tối/sáng
        saturated = (sat > 0.15) & (lightness > 0.1) & (lightness < 0.95)
        color_ratio = np.mean(saturated)
        return color_ratio < 0.08
    except Exception:
        return False


@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...), lang: str = "en"):
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(image_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if not is_xray_image(image_path):
        os.remove(image_path)
        msg = (
            "Vui lòng tải lên ảnh X-quang ngực hợp lệ. Ảnh màu thông thường không được hỗ trợ."
            if lang == "vi"
            else "Please upload a valid chest X-ray image. Color photos are not supported."
        )
        return JSONResponse({"success": False, "error": msg, "error_code": "not_xray"}, status_code=400)

    try:
        result = ai_agent.analyze(image_path, OUTPUT_DIR, lang=lang)
        return JSONResponse({"success": True, "data": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/translate-report")
async def translate_report(
    diagnosis: str  = Form(...),
    confidence: float = Form(...),
    location: str   = Form("chest"),
    size: str       = Form("moderate"),
    side: str       = Form("unspecified"),
    lang: str       = Form("en"),
):
    """Sinh lại report theo ngôn ngữ mới, không cần chạy lại model."""
    try:
        from agents.safety_agent import SafetyAgent
        prompt = generate_prompt(
            diagnosis=diagnosis, confidence=confidence,
            location=location, size=size, side=side, lang=lang,
        )
        report = _decoder.generate_report(prompt)
        safe_out = SafetyAgent().run({"report": report}, lang=lang)
        return JSONResponse({"success": True, "report": safe_out["report"]})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)