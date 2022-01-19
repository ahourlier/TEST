import os
import time
import psutil
from flask.cli import load_dotenv

from app import create_app

try:
    import googleclouddebugger

    googleclouddebugger.enable()
except ImportError:
    pass

load_dotenv()

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=os.getenv("DEV_SERVER"))
    while True:
        time.sleep(2)
        print(
            f"first process memory in bytes: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2}"
        )  # in bytes
