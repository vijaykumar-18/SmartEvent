# SmartEvent

SmartEvent is an event discovery and ticket booking application with a FastAPI backend and React/Vite frontend.

## Run locally

### Backend

From PowerShell:

```powershell
Set-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `SECRET_KEY` in `backend/.env` to a randomly generated value of at least 32 characters. Start the API:

```powershell
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; its interactive documentation is at `http://localhost:8000/docs`. Sample events are seeded when the database is empty. Event creation is intentionally not exposed as a public API.

### Frontend

In a separate PowerShell window:

```powershell
Set-Location frontend
npm install
npm run dev
```

The Vite app runs at `http://localhost:5173`. Set `VITE_API_URL` in `frontend/.env.local` if the backend API is not at `http://localhost:8000/api`.

## Configuration

- `SECRET_KEY`: required JWT signing secret (minimum 32 characters).
- `DATABASE_URL`: SQLAlchemy database URL; defaults to a local SQLite database.
- `BASE_URL`: public backend base URL embedded in ticket QR codes.
- `ALLOWED_ORIGINS`: comma-separated frontend origins allowed by CORS; defaults to `http://localhost:5173`.
- `VITE_API_URL`: frontend API URL; defaults to `http://localhost:8000/api`.

Event reminders are generated as in-app notifications by the backend process when confirmed bookings are for events within the next 24 hours. Run a single backend worker unless reminder delivery is moved to a dedicated scheduler.