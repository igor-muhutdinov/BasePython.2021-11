import logging
import random
from http import HTTPStatus
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from sqlalchemy.exc import DatabaseError, IntegrityError

from models.db import db
from models.library import Book, Author


log = logging.getLogger()
library_app = Blueprint(name="library_app", import_name=__name__)


@library_app.route("/", endpoint="main_page")
def main_page():
    books = Book.query.all()
    book = None
    if books:
        book = random.choice(books)
    return render_template("library/index.html", book=book)


@library_app.route("/books/", endpoint="books")
def get_books():
    books = Book.query.all()
    return render_template("library/books.html", books=books)


@library_app.route("/books/<int:book_id>/",
                   methods=["GET", "DELETE"],
                   endpoint="book_details")
def get_book(book_id: int):
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        raise NotFound(f"No book for id {book_id}")

    if request.method == "GET":
        return render_template("library/book_details.html", book=book)

    # if method="DELETE":
    db.session.delete(book)
    try:
        db.session.commit()
    except DatabaseError:
        log.exception("Could not delete book %, got database error", book)
        db.session.rollback()
        raise InternalServerError("Error deleting book")
    return "", HTTPStatus.NO_CONTENT


@library_app.route("/books/add/", methods=["GET", "POST"], endpoint="book_add")
def create_book():
    if request.method == "GET":
        authors = Author.query.all()
        return render_template("library/book_add.html", authors=authors)

    author_id = request.form.get("author-id")
    if not author_id:
        raise BadRequest("Please provide author!")

    book_title = request.form.get("book-title")
    if not book_title:
        raise BadRequest("Please provide book title!")

    book = Book(title=book_title, author_id=author_id)
    db.session.add(book)
    try:
        db.session.commit()
    except IntegrityError:
        log.exception("Could not add book, got integrity error")
        db.session.rollback()
        raise BadRequest("Error adding new book, probably the title is not unique")
    except DatabaseError:
        log.exception("Could not add book, got database error")
        db.session.rollback()
        raise InternalServerError("Error adding new book")

    return redirect(url_for("library_app.book_details", book_id=book.id))


@library_app.route("/authors/", endpoint="authors")
def get_authors():
    authors = Author.query.all()
    return render_template("library/authors.html", authors=authors)


@library_app.route("/authors/<int:author_id>/",
                   methods=["GET", "DELETE"],
                   endpoint="author_details")
def get_author(author_id: int):
    author = Author.query.filter_by(id=author_id).one_or_none()
    if author is None:
        raise NotFound(f"No author for id {author_id}")
    if request.method == "GET":
        books = Book.query.filter_by(author_id=author_id).all()
        return render_template("library/author_details.html", author=author, books=books)

    # if method="DELETE":
    db.session.delete(author)
    try:
        db.session.commit()
    except DatabaseError:
        log.exception("Could not delete author %, got database error", author)
        db.session.rollback()
        raise InternalServerError("Error deleting author")
    return "", HTTPStatus.NO_CONTENT


@library_app.route("/authors/add/", methods=["GET", "POST"], endpoint="author_add")
def create_author():
    if request.method == "GET":
        return render_template("library/author_add.html")

    author_name = request.form.get("author-name")
    if not author_name:
        raise BadRequest("Please provide author name!")

    author = Author(name=author_name)
    db.session.add(author)
    try:
        db.session.commit()
    except IntegrityError:
        log.exception("Could not add author, got integrity error")
        db.session.rollback()
        raise BadRequest("Error adding new author, probably the name is not unique")
    except DatabaseError:
        log.exception("Could not add author, got database error")
        db.session.rollback()
        raise InternalServerError("Error adding new author")

    return redirect(url_for("library_app.author_details", author_id=author.id))
