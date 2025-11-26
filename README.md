## Certificate Upload Assistant – Django + OpenAI Agent Builder + ChatKit

This project is a **full Django web app** that embeds an OpenAI **Agent Builder workflow** using **ChatKit**.

On your laptop, it gives you a beautiful, single‑page UI where:

- You chat with your OpenAI Agent directly inside your own site.
- The Agent is defined in **Agent Builder** and referenced by a `WORKFLOW_ID`.
- The frontend uses **TailwindCSS** for a clean, modern design.
- The backend is plain **Django**, so you can extend it however you like.

> This repository is designed to be easy to clone, configure, and run locally.  
> Follow the steps below carefully and you’ll have it running in a few minutes.

---

## 1. Features Overview

- **Django backend**
  - Simple project structure: one app called `certificates` and a single `home` view.
  - ChatKit session endpoint (`/api/chatkit/session/`) that creates a ChatKit session bound to your Agent Builder workflow.
  - Environment‑based configuration for OpenAI keys and workflow ID.

- **OpenAI integration**
  - Uses the official `openai` Python SDK.
  - Reads `OPENAI_API_KEY` and `WORKFLOW_ID` from environment variables / `.env`.
  - The ChatKit widget on the homepage talks directly to your **Agent Builder** workflow.

- **Modern UI**
  - TailwindCSS (via CDN) for a dark, minimal, responsive layout.
  - Centered “Upload your certificate” shell with an embedded ChatKit chat area.

---

## 2. Project Structure (high level)

```text
Django/
├─ certificate_project/      # Django project (settings, URLs, WSGI)
├─ certificates/             # App that hosts the views and URLs
│  └─ views.py               # home page + ChatKit session endpoint
├─ templates/
│  └─ home.html              # Tailwind + ChatKit web component
├─ manage.py                 # Django entrypoint
├─ requirements.txt          # Python dependencies
└─ .env                      # Your secrets (you create this)
```

You mainly interact with:

- `manage.py` – for running Django commands.  
- `certificates/views.py` – backend logic, ChatKit session endpoint.  
- `templates/home.html` – page layout and ChatKit embed.  
- `.env` – local environment configuration (not committed to GitHub).

---

## 3. Prerequisites

Please make sure you have:

- **Python 3.11+** (Python 3.13 is recommended – the project was set up with it).
- **pip** available on your PATH.
- An **OpenAI account** with:
  - A secret API key.
  - An **Agent Builder workflow** (copy its Workflow ID).

Optional but recommended:

- **Virtual environment** (via `python -m venv .venv`) to avoid polluting your global site‑packages.

---

## 4. Local Setup – Step by Step

Run the following commands in a terminal **from the project root folder** (where `manage.py` lives).

### 4.1. Create and activate a virtual environment (recommended)

Windows (PowerShell):

```powershell
cd "C:\path\to\Django-app"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
cd /path/to/Django-app
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `django` – web framework.  
- `openai` – OpenAI Python SDK.  
- `python-dotenv` – for loading `.env`.  
- `requests` – used for the ChatKit sessions HTTP call.

### 4.3. Create your `.env` file

In the project root, create a file named **`.env`** (no extension) and add:

```text
OPENAI_API_KEY=sk-...your-real-key-here...
WORKFLOW_ID=wf_6923a32204e48190b8586299a7e282870d0a26390fd91f66
```

> Replace the API key with your **own** OpenAI key.  
> Replace `WORKFLOW_ID` if you use a different workflow.

The app uses `python-dotenv` to read this file automatically when you run `manage.py`.

### 4.4. Apply database migrations

```bash
python manage.py migrate
```

You will see Django create the default SQLite database (`db.sqlite3`).

### 4.5. Start the development server

```bash
python manage.py runserver
```

You should see something like:

```text
Starting development server at http://127.0.0.1:8000/
```

Now open a browser and visit: **http://127.0.0.1:8000/**  
You’ll see the “Upload your certificate” page with the embedded ChatKit chat.

---

## 5. How the OpenAI / ChatKit integration works

### 5.1. ChatKit session endpoint

When the page loads, a small JavaScript snippet in `home.html`:

1. Waits for the `openai-chatkit` web component to be registered.
2. Creates the `<openai-chatkit>` element and configures it with `setOptions`.
3. The `getClientSecret` callback performs a `POST` request to:

```text
/api/chatkit/session/
```

### 5.2. Django view

The `create_chatkit_session` view in `certificates/views.py`:

- Reads `OPENAI_API_KEY` and `WORKFLOW_ID` from the environment.
- Calls the OpenAI `chatkit/sessions` HTTP endpoint with those values.
- Returns the `client_secret` JSON back to the browser.

The ChatKit widget then uses that `client_secret` to connect directly to your Agent Builder workflow. All subsequent messages from the browser go straight to OpenAI; Django just acts as the secure session creator.

---

## 6. Customising the UI

The main page lives in `templates/home.html`. You can easily tweak:

- Headline / description text.
- Layout and colours (via Tailwind utility classes).
- Container size (change the height/width around the chat container).

Because Tailwind is loaded from the CDN, you do **not** need a Node/Tailwind build pipeline just to try this locally.

---

## 7. Running the Project on Another Machine

If a friend or teammate wants to run this project on their laptop:

1. **Clone the repo**

   ```bash
   git clone https://github.com/GS-Tejas-hub/Django-app.git
   cd Django-app
   ```

2. **Create a virtual environment and install requirements**

   ```bash
   python -m venv .venv
   # Activate it, then:
   pip install -r requirements.txt
   ```

3. **Create their own `.env`** with their **own** OpenAI API key and (optional) workflow ID.
4. Run:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/` and start chatting with the Agent.

---

## 8. Pushing this project to GitHub

If you created this project locally first and want to push it to your GitHub repo (`https://github.com/GS-Tejas-hub/Django-app.git`):

```bash
cd /path/to/Django-app
git init
git add .
git commit -m "Initial Django + ChatKit project"
git branch -M main
git remote add origin https://github.com/GS-Tejas-hub/Django-app.git
git push -u origin main
```

After that, anyone can clone the repo and follow the setup instructions above.

---

## 9. Notes and Tips

- **Do not commit your `.env`** file or actual API keys to GitHub.
- Keep `DEBUG=True` only in development. For production you’ll need proper static/media hosting and HTTPS.
- If ChatKit ever refuses to respond, check:
  - Your `.env` values.
  - That your workflow is deployed and the ID matches.
  - The browser console and Django logs for detailed error messages.

Enjoy building with Django + OpenAI! If you want to extend this, good next steps are:

- Add your own database models to store processed certificates.  
- Add authentication so each user gets their own chat history.  
- Hook the Agent up to more tools (code interpreter, web search, etc.) inside Agent Builder.


