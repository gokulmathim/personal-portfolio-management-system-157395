import json
import os
from app import app, api  # the app and api variables are created in app/__init__.py via create_app()

"""
PUBLIC_INTERFACE
Utility script to generate and write OpenAPI JSON for the running Flask-Smorest API.

This script reuses the Api instance that already has all blueprints registered to ensure the
generated spec includes every endpoint and tag.

Output:
  - interfaces/openapi.json
"""

with app.app_context():
    openapi_spec = api.spec.to_dict()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
