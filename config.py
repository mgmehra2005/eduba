import os
import dotenv


class Config:
    dotenv.load_dotenv()
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    # Database settings (read from environment if present)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "eduba")
    DEBUG = False
    



class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    def __init__(self):
        if not os.environ.get("SECRET_KEY"):
            raise ValueError("SECRET_KEY environment variable must be set in production")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

# if __name__ == "__main__":
#     c = Config()
#     print("SECRET_KEY:", c.SECRET_KEY)
