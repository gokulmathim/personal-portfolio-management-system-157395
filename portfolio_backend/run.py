from app import create_app

app = create_app()

if __name__ == "__main__":
    # Bind to all interfaces with default port for container usage
    app.run(host="0.0.0.0", port=5000)
