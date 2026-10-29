"""Site settings: the Tableau Public views the app embeds and the two project links.

Each value can be overridden with an environment variable of the same name, so a
hosting service can set them without editing this file. Nothing here is secret.
"""
import os

# The published Tableau Public views, exactly as shared.
TABLEAU_DASHBOARD_URL = os.environ.get(
    "TABLEAU_DASHBOARD_URL",
    "https://public.tableau.com/views/EVMARKET-STORY_17932562476300/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link",
)
TABLEAU_STORY_URL = os.environ.get(
    "TABLEAU_STORY_URL",
    "https://public.tableau.com/views/EVMARKET-STORY1/Story1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link",
)

# The one overall Demo Link and GitHub Link for the project. They stay as these
# placeholders until the real URLs exist; the footer only links a value that is a URL.
DEMO_URL = os.environ.get("DEMO_URL", "[PUBLIC_DEMO_URL_PENDING]")
GITHUB_URL = os.environ.get("GITHUB_URL", "[GITHUB_REPOSITORY_URL_PENDING]")
