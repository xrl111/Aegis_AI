from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import students, overview, feedback

app = FastAPI(
    title="Aegis AI API",
    description="Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học",
    version="1.0.0"
)

# Cấu hình CORS để Frontend (Vue/Vite) có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên giới hạn cụ thể domain (VD: localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các routes
app.include_router(overview.router)
app.include_router(students.router)
app.include_router(feedback.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aegis AI Backend API. Visit /docs for Swagger UI."}
