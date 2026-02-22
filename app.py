from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = 'library-secret-key-change-in-production'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


def parse_date(date_str):
    """Convert 'YYYY-MM-DD' string to a date object, or return None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


@app.route('/')
def home():
    sort = request.args.get('sort', 'title')
    search = request.args.get('q', '').strip()

    query = db.session.query(Book).join(Author)

    if search:
        pattern = f'%{search}%'
        query = query.filter(
            db.or_(Book.title.ilike(pattern), Author.name.ilike(pattern))
        )

    if sort == 'author':
        query = query.order_by(Author.name.asc(), Book.title.asc())
    else:
        query = query.order_by(Book.title.asc())

    books = query.all()
    return render_template('home.html', books=books, sort=sort, search=search)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    success = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birth_date = parse_date(request.form.get('birth_date'))
        date_of_death = parse_date(request.form.get('date_of_death'))

        if not name:
            flash('Author name is required.', 'error')
        else:
            new_author = Author(
                name=name,
                birth_date=birth_date,
                date_of_death=date_of_death
            )
            db.session.add(new_author)
            db.session.commit()
            success = f'Author "{name}" was successfully added to the library!'

    return render_template('add_author.html', success=success)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.order_by(Author.name).all()
    success = None

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        isbn = request.form.get('isbn', '').strip()
        publication_year = request.form.get('publication_year') or None
        author_id = request.form.get('author_id')

        if not title or not isbn or not author_id:
            flash('Title, ISBN, and Author are required.', 'error')
        else:
            new_book = Book(
                title=title,
                isbn=isbn,
                publication_year=int(publication_year) if publication_year else None,
                author_id=int(author_id)
            )
            db.session.add(new_book)
            db.session.commit()
            success = f'"{title}" was successfully added to the library!'

    return render_template('add_book.html', authors=authors, success=success)


if __name__ == '__main__':
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)