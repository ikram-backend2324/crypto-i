# Forge — AI Business Plan Studio

Django + Django templates + SQLite. Generates a structured 10-section business
plan from a single idea, in the language the user writes in. AI via OpenRouter
(`deepseek/deepseek-v4-flash`). 3D hero built with Three.js.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env .env            # then edit .env and paste your OPENROUTER_API_KEY
python manage.py migrate
python manage.py create_default_superuser
python manage.py runserver
```
Open http://127.0.0.1:8000 — admin at /admin/.

## Deploy on Render
- **Build command:**
  `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_default_superuser`
- **Start command:**
  `gunicorn crypto_research_tool.wsgi:application`
- Add the variables from `.env` under Render → Environment.

Note: Render's free tier uses an ephemeral disk, so the SQLite DB resets on
redeploy. `create_default_superuser` re-creates the admin each deploy.
