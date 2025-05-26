from fastapi import FastAPI
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Assicura che .env venga caricato ANCHE nel processo uvicorn --reload
dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')
logging.info(f"PATH: {dotenv_path}")
load_dotenv(dotenv_path)


from app.routes.documents import router as documents_router
from app.routes.ai_outputs import router as ai_outputs_router
from app.routes.activity_logs import router as activity_logs_router
from app.routes.courses import router as courses_router

app = FastAPI(title="StudIA API", version="0.1.0")

# Include Routers
app.include_router(documents_router)
app.include_router(ai_outputs_router)
app.include_router(activity_logs_router)
app.include_router(courses_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to StudIA API!"}
