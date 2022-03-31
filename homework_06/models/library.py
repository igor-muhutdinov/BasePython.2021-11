from datetime import datetime
from sqlalchemy import func
from models.db import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author_id = db.Column(db.ForeignKey('author.id'), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
