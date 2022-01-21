import os
from flask.cli import load_dotenv
from app import create_app

try:
    import googleclouddebugger

    googleclouddebugger.enable()
except ImportError:
    pass

load_dotenv()

# Profiler initialization. It starts a daemon thread which continuously
# collects and uploads profiles. Best done as early as possible.
try:
    import googlecloudprofiler
    # service and service_version can be automatically inferred when
    # running on App Engine. project_id must be set if not running
    # on GCP.
    googlecloudprofiler.start(verbose=3)
except (ValueError, NotImplementedError) as exc:
    print(exc)  # Handle errors here

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=os.getenv("DEV_SERVER"))
