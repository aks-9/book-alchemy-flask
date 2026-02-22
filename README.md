# Book Alchemy

A personal digital library built with Flask and SQLAlchemy. Add authors and books, search your collection, sort by title or author, and remove books you've donated or passed on.

## Features

- **Browse** your library, sorted by title or author
- **Search** by book title or author name (case-insensitive, partial match)
- **Add authors** with optional birth/death dates
- **Add books** with ISBN, publication year, and author
- **Delete books** — if the deleted book was the author's only entry, the author is removed too
- **Book covers** fetched automatically from Open Library using the ISBN

## Project structure

```
.
├── app.py            # Flask routes
├── data_models.py    # SQLAlchemy models (Author, Book)
├── 
├── 
├── requirements.txt
├── data/
│   └── library.sqlite
└── templates/
    ├── base.html
    ├── home.html
    ├── add_author.html
    └── add_book.html
```

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd book-alchemy

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app (creates the database automatically on first run)
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Running the tests

```bash
pytest test_app.py -v
```

All tests use an isolated in-memory SQLite database and leave the production database untouched.

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Home — browse, search, sort |
| GET | `/?q=<term>` | Filter by title or author |
| GET | `/?sort=author` | Sort by author name |
| GET | `/add_author` | Add-author form |
| POST | `/add_author` | Create a new author |
| GET | `/add_book` | Add-book form |
| POST | `/add_book` | Create a new book |
| POST | `/book/<id>/delete` | Delete a book (and its author if no books remain) |

## Tech stack

| Layer | Technology |
|-------|-----------|
| Web framework | Flask 3.1 |
| ORM / database | Flask-SQLAlchemy 3.1 + SQLite |
| Templates | Jinja2 |
