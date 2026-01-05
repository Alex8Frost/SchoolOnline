from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from api.endpoints import companies

app = FastAPI(title="PyLearn", version="0.1.0")

# CORS для локальной разработки
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(companies.router)

# Статические файлы и фронтенд
frontend_path = Path(__file__).parent.parent / "frontend"

@app.get("/")
async def serve_index():
    """Обслуживает главную страницу фронтенда."""
    return FileResponse(str(frontend_path / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)