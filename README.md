# EV Adoption Intelligence

An intelligent analysis service and FastAPI backend for querying and extracting insights from Electric Vehicle (EV) adoption datasets using LLM-augmented analytics.

---

## 🚀 Features

- **FastAPI Backend**: Fast, asynchronous REST API with automatic interactive OpenAPI / Swagger documentation.
- **Dataset Analysis**: Analyzes cleaned EV adoption records (`EV_Adoption_Dataset_Recleaned.xlsx`).
- **LLM Insights Service**: Natural language question-answering over EV metrics, adoption trends, and regional breakdowns.
- **CORS Enabled**: Configured for seamless integration with frontend dashboards or external clients.

---

## 📁 Project Structure

```text
EV_Adoption_Intelligence/
├── backend/
│   ├── app/
│   │   ├── api/            # API route definitions (/api/chat, /api/health)
│   │   ├── models/         # Pydantic data schemas & request/response models
│   │   ├── prompts/        # System prompts and instructions for LLM
│   │   ├── services/       # Data processing & LLM query services
│   │   ├── config.py       # Configuration and environment management
│   │   └── main.py         # FastAPI application entry point
│   ├── data/
│   │   └── raw/            # Cleaned EV dataset (.xlsx)
│   ├── tests/              # Test suite
│   ├── .env.example        # Environment variable template
│   └── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- `pip` or `venv`

### 2. Setup Virtual Environment & Install Dependencies
```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` inside the `backend/` directory:
```bash
cp .env.example .env
```
Update `.env` with your LLM provider credentials:
```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TIMEOUT_SECONDS=60
BACKEND_URL=http://localhost:8000
DATA_PATH=data/raw/EV_Adoption_Dataset_Recleaned.xlsx
```

### 4. Running Locally
Run the server with Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```

Once running:
- **API Root**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`
- **Chat Endpoint**: `POST http://localhost:8000/api/chat`

---

## 🚢 Deployment

### 1. GitHub Repository
Repository: [https://github.com/adityaakula19-star/EV-INTEL](https://github.com/adityaakula19-star/EV-INTEL)

To push changes:
```bash
git add .
git commit -m "Update application"
git push
```

### 2. Live Cloud Deployment (Render - Free)
This repository includes a `render.yaml` blueprint for automatic deployment on Render:

1. Sign up / Log in to [Render](https://dashboard.render.com/).
2. Click **New +** → **Blueprint**.
3. Connect your GitHub account and select **`adityaakula19-star/EV-INTEL`**.
4. Set your environment variable:
   - `LLM_API_KEY`: *(your LLM API key)*
5. Click **Apply**. Render will build and deploy the API with a free public URL (e.g., `https://ev-adoption-intelligence.onrender.com`).

### 3. Railway / Other Cloud Hosts
You can also deploy directly via [Railway](https://railway.app/):
1. Create a new project on Railway and select **Deploy from GitHub repo**.
2. Select `EV-INTEL`. Railway will detect the included `Dockerfile` and `Procfile`.
3. Add `LLM_API_KEY` under the service **Variables** tab.

