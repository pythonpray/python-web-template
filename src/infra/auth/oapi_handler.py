from src.infra.logger import app_logger
from src.settings.config import get_settings

oapi_auth = get_settings().oapi


class OApiHandler:
    @staticmethod
    def verify_api_key(request) -> bool:
        """验证API密钥"""
        try:
            api_key = request.headers.get("X-API-Key")
            if not api_key:
                app_logger.info(f"cant get api key from url: {request.url}")
                return False
            return True
        except Exception as e:
            app_logger.error(f"Error verifying API key: {str(e)}")
            return False
