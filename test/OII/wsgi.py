"""
WSGI entry point.

Run app.py for dev; this for deployment.
"""

from server import app

if __name__ == "__main__":
    app.run()
