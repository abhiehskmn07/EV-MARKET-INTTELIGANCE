"""Flask front end for the Electric Vehicle Market Intelligence Tableau dashboard and story."""
import re

from flask import Flask, render_template

import config

app = Flask(__name__)

# The KPI cards on the published dashboard, with the values it shows (checked against the
# dataset in analysis/validation_report.md and analysis/published_check.md).
KPIS = [
    {"value": "772.6M", "label": "Annual sales units", "note": "sum over 2018-2026 model years"},
    {"value": "324.3 km", "label": "Average range", "note": "per vehicle record"},
    {"value": "$65,010", "label": "Average price", "note": "USD"},
    {"value": "169.9 kW", "label": "Average motor power", "note": "per vehicle record"},
    {"value": "3.98 / 5", "label": "Average safety rating", "note": "stars"},
]

GOALS = [
    "Compare EV sales across 15 vehicle categories and 200 manufacturers.",
    "Rank manufacturers by sales and market share.",
    "See how battery chemistry relates to durability and degradation.",
    "Compare driving range and battery capacity with price.",
    "Map where vehicles are manufactured and which regions buy them.",
    "Turn the evidence into recommendations for product positioning and sustainable mobility research.",
]

DATASET = [
    {"value": "100,000", "label": "vehicle records"},
    {"value": "37", "label": "columns"},
    {"value": "200", "label": "manufacturers"},
    {"value": "15", "label": "vehicle categories"},
    {"value": "10", "label": "manufacturing countries"},
    {"value": "7", "label": "market regions"},
    {"value": "5", "label": "battery types"},
    {"value": "2018-2026", "label": "model years"},
]

VISUALS = [
    {"title": "Top Summary KPIs", "chart": "KPI cards",
     "text": "Total annual sales units with average motor power, price, range and safety rating."},
    {"title": "Global EV Map", "chart": "Filled map",
     "text": "Annual sales units by manufacturing country, shaded from 75.6M to 78.9M units."},
    {"title": "Sales Trend by Year", "chart": "Line chart",
     "text": "Annual sales units for each market region across the 2018 to 2026 model years."},
    {"title": "Sales By Category", "chart": "Horizontal bar",
     "text": "Annual sales units by vehicle category, sorted from highest to lowest."},
    {"title": "Price vs Range", "chart": "Scatter plot",
     "text": "Price against driving range for each vehicle record, by category and manufacturer."},
    {"title": "Top Models by Motor Power", "chart": "Packed bubbles",
     "text": "The 15 model names with the most powerful motors."},
    {"title": "Market Share by Region", "chart": "Pie chart",
     "text": "Share of annual sales units by market region and drivetrain (AWD, FWD, RWD)."},
    {"title": "Manufacturer Market Share", "chart": "Treemap",
     "text": "Annual sales units for the leading manufacturers."},
]

# Each figure below comes from analysis/validation_report.md.
FINDINGS = [
    {"title": "Category sets the price, range and battery size",
     "text": "Electric buses average $274,045 and 300 kWh; two-wheeler scooters average $2,531 and 3.3 kWh. "
             "Average range runs from 105 km (scooters) to 549 km (luxury sedans)."},
    {"title": "Small vehicles sell the most units",
     "text": "Two-wheeler scooters lead with 85.0M units (11.0% of all units), followed by sedans and compact SUVs. "
             "Buses, electric trucks and pickups together are 2.4% of units."},
    {"title": "Commercial vehicles save the most CO2 per vehicle",
     "text": "Buses, electric trucks and pickups save about 9 t of CO2 a year each, against 3 t for cars and "
             "1.6 t for two- and three-wheelers."},
    {"title": "Battery chemistry changes durability, not adoption",
     "text": "Solid-state packs lose 7.4% capacity in five years and LFP 10.1%, against about 14% for NMC, NCA and "
             "sodium-ion. Each chemistry's share stays within 2 points across model years, so the data shows no "
             "adoption trend."},
    {"title": "The market is fragmented",
     "text": "No manufacturer reaches 1%: the largest, SurgeWorks, holds 0.63% of units and the top 10 together hold 6.0%."},
    {"title": "Ratings barely differ",
     "text": "Customer ratings average 4.08 out of 5 and differ by only 0.02 between categories. Price tracks battery "
             "capacity (r = 0.84) far more than range (r = 0.28)."},
]

STORY_SCENES = [
    "Global Overview: KPIs & Performance",
    "Geographic Distribution: Global EV Map",
    "Sales Growth: Annual Trend Analysis",
    "Category Analysis: Vehicle Type Sales",
    "Pricing Strategy: Price vs Driving Range",
    "Market Leaders: Top Models & Power",
    "Battery Tech: Battery Degradation Matrix",
    "Market Share: Manufacturer Breakdown",
    "Regional Market Share: Global Distribution",
]


def embed_src(link):
    """Return the /views/ URL the <tableau-viz> tag needs, from any Tableau Public share link."""
    link = link.strip()
    found = re.search(r"/(?:viz|views)/([^/?#]+)/([^/?#]+)", link)
    if not found:
        return link
    return f"https://public.tableau.com/views/{found.group(1)}/{found.group(2)}"


@app.context_processor
def project_links():
    return {"demo_url": config.DEMO_URL, "github_url": config.GITHUB_URL}


@app.route("/")
def home():
    return render_template("index.html", kpis=KPIS, goals=GOALS, dataset=DATASET, visuals=VISUALS,
                           findings=FINDINGS, scenes=STORY_SCENES)


@app.route("/dashboard")
def dashboard():
    return render_template(
        "viz.html",
        kicker="Interactive dashboard",
        heading="EV Market Intelligence Dashboard",
        intro="Eight views of 100,000 electric vehicle records on one page: sales by category, country, region "
              "and model year, price against range, motor power and manufacturer share. Hover over any mark for "
              "exact values; the toolbar under the view can undo, reset, download or go full screen.",
        src=embed_src(config.TABLEAU_DASHBOARD_URL),
        share_url=config.TABLEAU_DASHBOARD_URL,
        setting="TABLEAU_DASHBOARD_URL",
    )


@app.route("/story")
def story():
    return render_template(
        "viz.html",
        kicker="Data story",
        heading="The EV Market Story",
        intro="Nine scenes, from the headline KPIs to regional market share. Click a caption at the top of the "
              "story, or use its arrows, to move between scenes.",
        src=embed_src(config.TABLEAU_STORY_URL),
        share_url=config.TABLEAU_STORY_URL,
        setting="TABLEAU_STORY_URL",
        scenes=STORY_SCENES,
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
