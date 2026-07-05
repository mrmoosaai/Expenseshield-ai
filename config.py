from dotenv import load_dotenv
import os

load_dotenv()

# ==========================================
# LLM SETTINGS
# ==========================================
LLM_CONFIG = {
    "model": "gemini-1.5-flash-latest",
    "api_key": os.getenv("GEMINI_API_KEY"),
}

# ==========================================
# EMAIL SETTINGS
# ==========================================
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "sender_email": os.getenv("SENDER_EMAIL"),
    "app_password": os.getenv("APP_PASSWORD"),
    "manager_email": os.getenv("MANAGER_EMAIL"),
}

# ==========================================
# SERVER SETTINGS
# ==========================================
SERVER_CONFIG = {
    "host": os.getenv("HOST", "localhost"),
    "port": int(os.getenv("PORT", "8880")),
    "reload": True,
}

# ==========================================
# BUSINESS RULES
# ==========================================
AUTO_APPROVE_THRESHOLD = int(os.getenv("AUTO_APPROVE_THRESHOLD", "100"))
