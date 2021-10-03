import os
import shutil

# App credentials.
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = os.environ.get("APP_PORT", "7000")

# Logs.
APP_LOG_PATH = os.environ.get("APP_LOG_PATH", "/tmp/capstone1-local/logs")
APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "DEBUG")

APP_TEMP_PATH = os.environ.get("APP_TEMP_PATH", "/tmp/capstone1-local/data")

# Create paths if not exist.
for path in [APP_TEMP_PATH, APP_LOG_PATH]:
    shutil.rmtree(path)
    os.mkdir(path)
