from fastapi import FastAPI
from app.routes.documents import router as documents_router
from app.routes.ai_outputs import router as ai_outputs_router
from app.routes.activity_logs import router as activity_logs_router

app = FastAPI(title="StudIA API", version="0.1.0")

# Include Routers
app.include_router(documents_router)
app.include_router(ai_outputs_router)
app.include_router(activity_logs_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to StudIA API!"}
