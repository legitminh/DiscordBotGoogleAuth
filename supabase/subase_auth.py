import secrets
import uuid
from datetime import datetime, timedelta
from supabase import create_client
import os
from urllib.parse import urlencode

# Supabase configuration
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtwdm1jZGl5cWZianRhbnV0ZWZiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDg0NTY1OSwiZXhwIjoyMDYwNDIxNjU5fQ.dGzWZLAU7R3jk7vLQkf9tPi_ipwxFMc3EHKAfBRups8"
SUPABASE_URL = "https://kpvmcdiyqfbjtanutefb.supabase.co"
AUTH_SERVER_URL = "https://your-auth-server.com/auth-callback"  # Your server URL

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def generate_auth_link(user_identifier: str, expiration_hours: int = 1) -> dict:
    """
    Generate a unique authentication link with a secret code
    
    Args:
        user_identifier: Email, username, or any user identifier
        expiration_hours: How many hours until the link expires
    
    Returns:
        dict: Contains the generated link and secret code
    """
    try:
        # Generate a secure random secret code
        secret_code = secrets.token_urlsafe(32)
        
        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
        
        # Prepare data for Supabase
        auth_data = {
            "secret_code": secret_code,
            "user_identifier": user_identifier,
            "expires_at": expires_at.isoformat(),
            "is_active": True,
            "is_used": False
        }
        
        # Insert into Supabase
        response = supabase.table("auth_links").insert(auth_data).execute()
        
        if not response.data:
            raise Exception("Failed to create auth link in database")
        
        # Create the authentication link
        query_params = {
            "code": secret_code,
            "user": user_identifier
        }
        
        auth_link = f"https://yourapp.com/auth/verify?{urlencode(query_params)}"
        
        return {
            "success": True,
            "auth_link": auth_link,
            "secret_code": secret_code,
            "expires_at": expires_at.isoformat(),
            "user_identifier": user_identifier
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Example usage
if __name__ == "__main__":
    result = generate_auth_link("user@example.com", expiration_hours=2)
    
    if result["success"]:
        print("✅ Authentication link generated successfully!")
        print(f"🔗 Link: {result['auth_link']}")
        print(f"🔐 Secret Code: {result['secret_code']}")
        print(f"⏰ Expires: {result['expires_at']}")
    else:
        print(f"❌ Error: {result['error']}")