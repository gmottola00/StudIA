from supabase import create_client
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Carica variabili d'ambiente da backend/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
logging.info(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")

from app.services.relational_db_manager.document_manager import DocumentManager
from app.services.relational_db_manager.ai_output_manager import AIOutputManager
from app.services.relational_db_manager.activity_log_manager import ActivityLogManager
from app.services.relational_db_manager.course_manager import CourseManager


class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client = create_client(url, key)
        self.documents = DocumentManager(self.client)
        self.ai_outputs = AIOutputManager(self.client)
        self.activity_logs = ActivityLogManager(self.client)
        self.courses = CourseManager(self.client)