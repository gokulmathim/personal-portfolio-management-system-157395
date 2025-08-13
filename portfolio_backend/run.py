import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    """
    Entrypoint to run the Flask application.

    Environment:
      - PORT: The port to bind to (defaults to 3001 for container readiness expectations).
      - HOST: The host interface to bind to (defaults to 0.0.0.0).
    """
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3001"))
    # Bind to all interfaces with a default port aligned to the orchestrator's readiness check
    app.run(host=host, port=port)
