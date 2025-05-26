from app.services.supabase_service import SupabaseService

# Singleton SupabaseService instance
_supabase_service = SupabaseService()

def get_supabase_service():
    """Dependency to get SupabaseService instance"""
    return _supabase_service
