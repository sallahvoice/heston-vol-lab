import os


def pytest_configure():
    os.environ.setdefault("ENVIRONMENT", "dev")
    os.environ.setdefault("LOG_LEVEL", "INFO")
    os.environ.setdefault("DB_URL", "sqlite:///tmp.db")
    os.environ.setdefault("DB_USER", "test")
    os.environ.setdefault("DB_PASSWORD", "test")
    os.environ.setdefault("DB_PORT", "5432")
    os.environ.setdefault("DB_POOL_SIZE", "4")