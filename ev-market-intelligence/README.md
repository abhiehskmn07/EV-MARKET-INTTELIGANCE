# EV Market Intelligence website

A small Flask site that presents the project and embeds the published Tableau Public dashboard and story.

| Route | Page |
| --- | --- |
| `/` | Project overview, headline KPIs, dataset summary, dashboard views, key findings, story scenes |
| `/dashboard` | The Tableau Public dashboard, embedded |
| `/story` | The Tableau Public story, embedded |

```
app.py              routes and page content
config.py           Tableau view links, Demo Link and GitHub Link
templates/          base.html (header, footer), index.html, viz.html (embeds), 404.html
static/css/         style.css (navy, white and green theme)
```

## Run locally

From this folder:

```bash
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe app.py
```

Open https://ev-market-intteligance.onrender.com

## Settings

All settings are in `config.py` and can be overridden with environment variables of the same name. None of them
are secret.

| Setting | Default |
| --- | --- |
| `TABLEAU_DASHBOARD_URL` | the supplied dashboard share link |
| `TABLEAU_STORY_URL` | the supplied story share link |
| `DEMO_URL` | `[PUBLIC_DEMO_URL_PENDING]` (shown as text; linked once it is a URL) |
| `GITHUB_URL` | `[GITHUB_REPOSITORY_URL_PENDING]` (shown as text; linked once it is a URL) |

The pages embed the views with Tableau's Embedding API v3 (`<tableau-viz>`), which keeps all Tableau
interactivity: tooltips, toolbar, story navigation and full screen. The share links are reduced to their
`/views/<workbook>/<sheet>` form for the embed. The "Open on Tableau Public" buttons use the links exactly as
supplied.

## Notes

- The embedded views come from Tableau Public. They need internet access and depend on the workbooks staying
  public. If a view cannot be loaded, the page says so.
- `app.py` runs Flask's development server with `debug=True`. For hosting, use gunicorn (below) and do not
  enable debug mode.

## Deploy

The site is **not deployed yet**; https://ev-market-intteligance.onrender.com only works on the computer running it. One way to host it
for free is Render, straight from the GitHub repository:

1. Push the repository to GitHub.
2. On render.com: **New > Web Service**, connect the repository.
3. Set **Root Directory** `ev-market-intelligence`, **Build Command** `pip install -r requirements.txt`,
   **Start Command** `gunicorn app:app`.
4. Once it is live, set the environment variables `DEMO_URL` (the Render URL) and `GITHUB_URL` (the repository
   URL), or put them in `config.py`.

`requirements.txt` installs gunicorn only on Linux and macOS, because gunicorn does not run on Windows.
