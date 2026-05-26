import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.student_routes import student_bp
    from app.routes.course_routes import course_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    return app
