from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class EmailSettings(BaseSettings):
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "wahegurusingh2002@gmail.com"
    SMTP_PASSWORD: str = "pbob qqhh gvdu rjox"
    # For Gmail, EMAIL_FROM must match SMTP_USERNAME
    EMAIL_FROM: EmailStr = "wahegurusingh2002@gmail.com"
    EMAIL_FROM_NAME: str = "BookSlot System"
    
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

# Create an instance of the settings
email_settings = EmailSettings()
