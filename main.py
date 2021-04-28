import os

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
