# Dependencies

This document explains how dependencies are managed in Battle Results Flask, what each package does, and how to add, remove, or update them.

---

## Table of Contents

1. [Tool: Pipenv](#tool-pipenv)
2. [The Two Key Files](#the-two-key-files)
   - [Pipfile](#pipfile)
   - [Pipfile.lock](#pipfilelock)
3. [The Virtual Environment](#the-virtual-environment)
4. [Runtime Dependencies](#runtime-dependencies)
5. [Dev-only Dependencies](#dev-only-dependencies)
6. [Common Tasks](#common-tasks)
7. [Dependencies Inside Docker](#dependencies-inside-docker)

---

## Tool: Pipenv

This project uses **Pipenv** as its package and virtual environment manager. It combines the roles of `pip` (installing packages) and `venv` (isolating them) into one tool, and adds deterministic locking so every developer and deployment gets identical package versions.

If `pipenv` is not on your PATH after installing it (common on Windows), use `python -m pipenv` as a drop-in replacement for every command in this document.

---

## The Two Key Files

### Pipfile

`Pipfile` is the **human-maintained** file. It declares the packages the project needs and nothing else:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-sqlalchemy = "*"
flask-assets = "*"
jsmin = "*"
python-dotenv = "*"
cssmin = "*"
libsass = "*"
flask-swagger-ui = "*"

[dev-packages]
autopep8 = "*"
pytest = "*"
pytest-flask = "*"
coverage = "*"

[requires]
python_version = "3.13"
```

Key points:

- **`[packages]`** — packages needed to run the application in any environment (development, production, Docker).
- **`[dev-packages]`** — packages needed only during development (linting, testing, coverage). They are never installed inside the Docker container.
- **`"*"`** — means "any version". Pipenv resolves and pins the actual version in `Pipfile.lock`, so `*` here just means "latest compatible" at the time of the last lock.
- **`[requires]`** — declares the minimum Python version. Pipenv will warn (or refuse) if the active Python doesn't match.

### Pipfile.lock

`Pipfile.lock` is the **machine-generated** file. It is produced by Pipenv and must never be edited by hand.

It records:
- The exact version of every package installed (including transitive dependencies — packages that your packages depend on).
- The SHA-256 hash of every downloaded file, so Pipenv can verify that what you install is byte-for-byte identical to what was locked.

This is what makes installs **reproducible**: two developers running `python -m pipenv install` a month apart will get the exact same environment, regardless of what was published to PyPI in between.

**Both files must be committed to version control.** `Pipfile` is your intent; `Pipfile.lock` is the guarantee.

---

## The Virtual Environment

When you run `python -m pipenv install` for the first time, Pipenv:

1. Creates a virtual environment (an isolated directory containing a private Python interpreter and its own `site-packages`).
2. Installs every package listed in `Pipfile.lock` into that private environment, not into the system Python.

The virtual environment is stored in `.venv/` inside the project root (this is configured by the `PIPENV_VENV_IN_PROJECT=1` convention, which Pipenv respects when a `.venv` folder already exists or is created there).

This isolation means:
- Installing or removing a package here has **no effect** on any other project or on the system Python.
- If the environment gets corrupted, you can delete `.venv/` and recreate it cleanly with `python -m pipenv install`.

You interact with the virtual environment in two ways:

```bash
# Option A: spawn a subshell with the venv activated
python -m pipenv shell
# now you can run: python app.py, pytest, etc.
exit   # leaves the subshell

# Option B: run a single command inside the venv without activating
python -m pipenv run python app.py
python -m pipenv run pytest
```

---

## Runtime Dependencies

These packages are installed in every environment (local and Docker) via `python -m pipenv install`.

| Package | Version (locked) | Why it's needed |
|---|---|---|
| **Flask** | 3.1.1 | Core web framework: routing, request/response lifecycle, blueprints, WSGI server |
| **Flask-SQLAlchemy** | 3.1.1 | Flask integration for SQLAlchemy; provides `db` instance, app context binding, and session management |
| **SQLAlchemy** | 2.0.41 | ORM that maps Python classes to SQLite tables; transitive dependency of Flask-SQLAlchemy |
| **Flask-Assets** | 2.1.0 | Asset pipeline: compiles SASS to CSS and bundles JS/CSS files; also manages cache-busting |
| **webassets** | 2.0 | Core asset bundling engine used by Flask-Assets (transitive dependency) |
| **libsass** | 0.23.0 | SASS/SCSS compiler; invoked by Flask-Assets on `.scss` files in `static/styles/` |
| **cssmin** | 0.2.0 | CSS minifier; applied after libsass compiles SCSS into plain CSS |
| **jsmin** | 3.0.1 | JavaScript minifier; applied to `static/js/*.js` files before bundling |
| **flask-swagger-ui** | 5.21.0 | Serves the Swagger UI interface at `/api/docs`, pointing at `static/swagger.json` |
| **python-dotenv** | 1.1.1 | Loads environment variables from `.env` into `os.environ` at startup |
| **Jinja2** | 3.1.6 | HTML templating engine (transitive dependency of Flask); used in `templates/` |
| **Werkzeug** | 3.1.3 | WSGI utilities underlying Flask: routing, dev server, request objects (transitive) |

### Where each package is used

| Package | Where in the codebase |
|---|---|
| Flask | `app.py`, all `routes/`, all `controllers/` |
| Flask-SQLAlchemy / SQLAlchemy | `config/database.py`, `db_models/battle_entry.py`, all controllers |
| Flask-Assets + libsass + cssmin + jsmin | `config/assets_registering.py` |
| flask-swagger-ui | `app.py` (Swagger blueprint registration) |
| python-dotenv | `config/database.py` (`load_dotenv()`) |
| Jinja2 | `templates/base.html`, `templates/index.html` (via `render_template`) |

---

## Dev-only Dependencies

These packages are installed only in local development environments via `python -m pipenv install --dev`. They are **not** present in the Docker container.

| Package | Version (locked) | Why it's needed |
|---|---|---|
| **pytest** | 8.4.1 | Test runner used for `tests/test_views.py` |
| **pytest-flask** | 1.3.0 | Pytest fixtures for Flask apps (e.g., `client` fixture in `test_views.py`) |
| **coverage** | 7.9.2 | Measures which lines of code are exercised by tests; used by `run_tests.py --coverage` |
| **autopep8** | 2.3.2 | Automatic Python code formatter following PEP 8 style |

> `tests/test_api.py` uses the standard-library `unittest` module and does not require pytest, but pytest can discover and run unittest-style test cases too.

---

## Common Tasks

### Install all dependencies (first time or after cloning)

```bash
# Runtime + dev packages
python -m pipenv install --dev
```

### Install runtime dependencies only (e.g., on a server)

```bash
python -m pipenv install
```

### Add a new runtime package

```bash
python -m pipenv install <package-name>
```

This installs the package, adds it to `[packages]` in `Pipfile`, and updates `Pipfile.lock`. Commit both files.

### Add a new dev-only package

```bash
python -m pipenv install --dev <package-name>
```

This adds it to `[dev-packages]` instead.

### Remove a package

```bash
python -m pipenv uninstall <package-name>
```

This uninstalls the package, removes it from `Pipfile`, and regenerates `Pipfile.lock`. Commit both files.

### Update all packages to their latest compatible versions

```bash
python -m pipenv update --dev
```

This resolves the latest versions allowed by `Pipfile`, reinstalls them, and regenerates `Pipfile.lock`.

### Update a single package

```bash
python -m pipenv update <package-name>
```

### Regenerate the lock file without changing the venv

Useful after editing `Pipfile` manually (e.g., changing a version constraint):

```bash
python -m pipenv lock
```

### Remove stale packages from the venv

Removes packages that are in the venv but no longer declared in `Pipfile.lock`:

```bash
python -m pipenv clean
```

### Recreate the virtual environment from scratch

```bash
# Delete the venv
python -m pipenv --rm

# Recreate it from the lock file
python -m pipenv install --dev
```

### Check for known security vulnerabilities

```bash
python -m pipenv check
```

### Show the full dependency tree

```bash
python -m pipenv graph
```

---

## Dependencies Inside Docker

The `Dockerfile` installs **runtime dependencies only** (no dev packages) directly into the container's system Python — no virtual environment is created inside the container, because the container itself provides the isolation:

```dockerfile
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
```

- `--system` — installs packages into the system Python instead of a venv.
- `--deploy` — fails the build if `Pipfile.lock` is out of sync with `Pipfile`, or if it was generated for a different Python version. This is a safety check that prevents deploying with a stale lock.

Dev packages (`autopep8`, `pytest`, `pytest-flask`, `coverage`) are intentionally excluded from the Docker image to keep it lean.

See [docker.md](docker.md) for the full Docker guide.
