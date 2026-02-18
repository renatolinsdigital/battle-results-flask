# Battle Results Flask

A REST API and minimal web UI for tracking game battle results, built with Flask and SQLAlchemy. Entries are displayed from newest to oldest.

![Application Screenshot](print/print.png)

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask |
| ORM | SQLAlchemy (SQLite) |
| Templating | Jinja2 |
| Styling | Sass (compiled via Flask-Assets) |
| API Docs | Swagger UI (`/api/docs`) |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/entries` | List all battle entries (newest first) |
| POST | `/entries` | Create a battle entry |
| GET | `/entries/<id>` | Get a single entry |
| PATCH | `/entries/<id>` | Partially update an entry |
| DELETE | `/entries/<id>` | Delete an entry |

### POST / PATCH payload fields

| Field | Type | Notes |
|---|---|---|
| `gameTag` | string | max 100 chars; immutable after creation |
| `player1Name` | string | max 100 chars |
| `player2Name` | string | max 100 chars; must differ from `player1Name` |
| `winnerName` | string | must equal `player1Name` or `player2Name` |
| `finishedDate` | string | PATCH only; format `YYYY-MM-DD HH:MM:SS` |

## Quick Start

**1. Configure environment**

```bash
cp .env.example .env
# Edit .env and set FLASK_SECRET_KEY to a strong random value
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**2. Install dependencies**

```bash
pip install pipenv
pipenv install
pipenv shell
```

**3. Run**

```bash
python app.py
```

- Web UI: http://localhost:8080
- API docs: http://localhost:8080/api/docs

## Docker

```bash
# Set FLASK_SECRET_KEY before starting
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
docker compose up --build
```

## Testing

```bash
# Run tests
python run_tests.py

# Run tests with coverage report
python run_tests.py --coverage
```

## Project Structure

```
app.py                  # Application entry point
config/
  flask.py              # Flask configuration (env vars)
  database.py           # SQLAlchemy setup
  assets_registering.py # JS/CSS bundle configuration
  status_codes.py       # HTTP status code constants
routes/
  index.py              # Web UI route (/)
  entries.py            # API routes (/entries)
controllers/
  entries.py            # Business logic for entries
db_models/
  battle_entry.py       # BattleEntry ORM model
tests/
  test_api.py           # API unit tests
  test_views.py         # View tests
static/
  swagger.json          # OpenAPI spec
docs/                   # Extended documentation
```

## License

See [LICENSE](LICENSE).
