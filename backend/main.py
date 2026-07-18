"""Aegis AI — FastAPI Application Entry Point.

Chạy server:
    cd backend
    uvicorn main:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import students, overview, feedback

app = FastAPI(
    title="Aegis AI — Early Warning System",
    description=(
        "Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học. "
        "Rule-based, Individual Baseline, Privacy-first."
    ),
    version="0.1.0",
)

# CORS — cho phép frontend Vue dev server kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # Vite dev server
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(overview.router, prefix="/api/overview", tags=["Overview"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])


@app.get("/api/health", tags=["System"])
def health_check() -> dict[str, str]:
    """Kiểm tra server đang chạy."""
    return {"status": "ok", "service": "aegis-ai"}
