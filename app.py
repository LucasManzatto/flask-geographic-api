from app import create_app
import secrets

app = create_app()
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.config["MAX_CONTENT_LENGTH"] = 1000 * 1000 * 1000

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
