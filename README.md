# MedAgent AI

Hệ thống phân tích ảnh X-quang ngực tự động sử dụng kiến trúc đa tác nhân (Multi-Agent System) kết hợp Deep Learning và LLM.

---

## Kiến trúc hệ thống

```
    Ảnh X-quang
         │
         ▼
┌─────────────────┐
│   Vision Agent  │  classify → segment → gradcam
└────────┬────────┘
         │ top_disease, confidence, visual_findings, heatmap
         ▼
┌──────────────────────┐
│  Explanation Agent   │  sinh báo cáo Findings + Impression
└────────┬─────────────┘
         │ report
         ▼
┌──────────────────┐
│   Safety Agent   │  kiểm tra vi phạm đạo đức y tế + gắn disclaimer
└────────┬─────────┘
         │
         ▼
     Kết quả cuối
```

### Các thành phần chính

| Thành phần | Vai trò |
|---|---|
| `VisionAgent` | Phân loại bệnh, phân vùng tổn thương, sinh heatmap Grad-CAM |
| `ExplanationAgent` | Sinh báo cáo y tế từ kết quả phân tích |
| `SafetyAgent` | Kiểm duyệt nội dung, loại bỏ chẩn đoán xác định, kê đơn, tiên lượng |
| `MedicalAgentOrchestrator` | Điều phối luồng 3 agents |

### Models

- **DenseNet121** (fine-tuned): phân loại 17 bệnh lý X-quang
- **ResNet** (ensemble): hỗ trợ phân loại
- **Grad-CAM**: sinh heatmap vùng nghi ngờ
- **BioGPT** (Microsoft): sinh báo cáo ngôn ngữ y tế (mặc định dùng template, bật bằng `USE_TEMPLATE_ONLY=False`)

---

## Cài đặt

### Yêu cầu

- Python 3.11+
- Node.js 18+ (cho frontend)
- pyenv (khuyến nghị)

### Backend

```bash
# Cài Python 3.11 qua pyenv
pyenv install 3.11.9
pyenv global 3.11.9

# Tạo và kích hoạt virtual environment
python -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm run build
```

### Cấu hình môi trường

Tạo file `.env` từ mẫu:

```bash
cp .env.exsample .env
```

Nội dung `.env`:

```env
# LLM (tùy chọn — để trống sẽ dùng fallback pipeline)
LLM_PROVIDER=        # openai | google | ollama
LLM_MODEL_NAME=      # gpt-4o-mini | gemini-1.5-flash | llama3
LLM_API_KEY=         # API key tương ứng

# Kaggle (chỉ cần nếu tải dữ liệu)
KAGGLE_USERNAME=
KAGGLE_KEY=
```

---

## Chạy ứng dụng

```bash
# Kích hoạt venv
source venv/bin/activate

# Khởi động backend
uvicorn app:app --port 8000 --reload
```

Truy cập: [http://localhost:8000](http://localhost:8000)

---

## API

| Endpoint | Method | Mô tả |
|---|---|---|
| `POST /analyze-image` | POST | Phân tích ảnh X-quang, param: `file`, `lang` (en/vi) |
| `POST /translate-report` | POST | Sinh lại báo cáo theo ngôn ngữ mới |
| `GET /test-samples` | GET | Danh sách ảnh mẫu theo category |
| `GET /outputs/{filename}` | GET | Truy cập ảnh kết quả / heatmap |

### Ví dụ response `/analyze-image`

```json
{
  "success": true,
  "data": {
    "status": "Abnormal",
    "diagnosis": "Pneumonia",
    "confidence": 0.82,
    "visual_findings": {
      "location": "lower lung zone",
      "size": "small",
      "side": "right lung"
    },
    "report": "Findings: ... Impression: ...",
    "heatmap_path": "outputs/heatmap_Pneumonia_20260101_120000.png",
    "output_image": "outputs/result_filename.png",
    "safety_reviewed": true
  }
}
```

---

## Tính năng Frontend

- Upload ảnh X-quang hoặc chọn từ ảnh mẫu có sẵn
- Kiểm tra ảnh có phải X-quang trước khi gửi (dựa trên HSL saturation)
- Hiển thị heatmap Grad-CAM, kết quả phân loại, báo cáo y tế
- Hỗ trợ 2 ngôn ngữ: Tiếng Việt / English (chuyển đổi realtime)

---

## Cấu trúc thư mục

```
medagent-ai/
├── agents/
│   ├── orchestrator.py       # Điều phối đa tác nhân
│   ├── vision_agent.py       # Phân tích thị giác
│   ├── explanation_agent.py  # Sinh báo cáo
│   ├── safety_agent.py       # Kiểm duyệt an toàn
│   └── tools/                # LangChain tools
├── models/
│   ├── classifier.py         # DenseNet121 + ResNet ensemble
│   ├── gradcam.py            # Grad-CAM heatmap
│   ├── segmenter.py          # Phân vùng tổn thương
│   ├── decoder.py            # BioGPT decoder
│   └── bridge.py             # Template báo cáo (EN/VI)
├── frontend/                 # React app
├── data/iu_xray/             # Dataset IU X-Ray
├── app.py                    # FastAPI server
└── config.py                 # Cấu hình
```

---

## Lưu ý

- Hệ thống **không thay thế** chẩn đoán của bác sĩ. Kết quả chỉ mang tính hỗ trợ nghiên cứu.
- BioGPT mặc định bị tắt (`USE_TEMPLATE_ONLY=True` trong `models/decoder.py`) để tiết kiệm tài nguyên. Bật lên nếu có GPU.
- LLM là tùy chọn — hệ thống hoạt động đầy đủ mà không cần cấu hình LLM.
