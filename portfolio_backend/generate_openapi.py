import json
import os
from app import app  # the app variable is created in app/__init__.py via create_app()
from flask_smorest import Api

# Build an Api instance from the existing app to access the spec
api = Api(app)

with app.app_context():
    openapi_spec = api.spec.to_dict()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
