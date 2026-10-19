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

## 🚢 Deploying to GitHub

To push this repository to GitHub:

1. Create a new repository on [GitHub](https://github.com/new) (e.g. `ev-adoption-intelligence`). Leave it empty (without initializing README or .gitignore).
2. Run the following commands from the root directory:
```bash
git add .
git commit -m "Initial commit: EV Adoption Intelligence backend"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
git push -u origin main
```
