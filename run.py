import os

from dotenv import load_dotenv
from sqlalchemy import text

from app.config import create_app, db

load_dotenv()

app = create_app()

if __name__ == "__main__":
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("Database connection successfull")
            db.create_all()
    except Exception as e:
        print(f"Database connection failed:{e}")

    port = int(os.getenv("FLASK_PORT", 2222))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, port=port)
