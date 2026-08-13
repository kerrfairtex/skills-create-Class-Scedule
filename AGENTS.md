# AGENTS.md

## Cursor Cloud specific instructions

### Product
Single Flask app: the **Class Schedule Management System (CSMS)** for the TRAC BSIT department. Python 3.12, Flask + Flask-SQLAlchemy + Flask-Login, embedded SQLite (`instance/schedule.db`, auto-created on startup). No Node/Docker/external services. See `README.md` for the module overview.

### Environment
- Python dependencies are installed into a virtualenv at `.venv` by the startup update script (`pip install -r requirements.txt`). Always run Python via `.venv/bin/python` (or activate `.venv`).
- The system package `python3-venv` is required to create `.venv` and is baked into the VM snapshot (not reinstalled by the update script). If `.venv` creation ever fails on a fresh pod, run `sudo apt-get install -y python3.12-venv`.

### Run the app (dev)
There is no `run.py`/`wsgi.py`; the app uses the `create_app` factory in `app/__init__.py`. Start the dev server with:
```
FLASK_APP="app:create_app" .venv/bin/python -m flask run --host=0.0.0.0 --port=5000
```
On first boot it creates `instance/`, `instance/backups/`, all SQLite tables, and seeds an admin account: **username `admin` / password `admin123`**. Login is at `/auth/login`; `/` redirects there.

### Lint / test / build
- No test suite, linter config, or build step exists in the repo. Route files use `# noqa` comments (flake8 style) but no flake8 config is committed.
- Smoke check that all modules import/compile: `.venv/bin/python -m compileall -q app config.py`.

### Non-obvious caveats
- `main` is a **partial scaffold**. Only the `auth` and `master` blueprints are fully implemented. The `schedule`, `views`, and `database` blueprints have minimal/empty `routes.py` (added so `create_app()` can import them), and only a small set of `app/templates/` exists (`base.html`, `auth/login.html`, `schedule/index.html`) — enough to boot and demonstrate the login → dashboard flow. Most `render_template(...)` calls in `app/master/routes.py` and `app/auth/routes.py` reference templates that do **not** exist yet, so those pages will raise `TemplateNotFound` until the templates are added. This is expected for the current scaffold, not an environment problem.
- `.devcontainer/` is a leftover, unrelated "Copilot CLI Calculator" Node template and does **not** apply to this Python app (ignore its port 3000 / `npm install`).
- Flask-WTF is installed but CSRF protection is not enabled in `create_app`, so plain HTML `POST` forms work without CSRF tokens.
