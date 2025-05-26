from supabase import create_client
from dotenv import load_dotenv
import os

from app.managers.document_manager import DocumentManager
from app.managers.ai_output_manager import AIOutputManager
from app.managers.activity_log_manager import ActivityLogManager

# Carica .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client = create_client(url, key)
        self.documents = DocumentManager(self.client)
        self.ai_outputs = AIOutputManager(self.client)
        self.activity_logs = ActivityLogManager(self.client)
