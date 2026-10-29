# Electric Vehicle Market Intelligence Dashboard

A Tableau project that analyses 100,000 electric vehicle records. It covers vehicle categories, manufacturers,
sales, pricing, battery technology, driving range, customer ratings, manufacturing countries and CO2 savings.
The dashboard and story are published to Tableau Public and embedded in a Flask website.

## Project links

| | |
| --- | --- |
| **Demo Link** | [PUBLIC_DEMO_URL_PENDING] |
| **GitHub Link** | https://github.com/abhiehskmn07/EV-MARKET-INTTELIGANCE |
| website URL | https://ev-market-intteligance.onrender.com |
| Tableau Dashboard | https://public.tableau.com/views/EVMARKET-STORY_17932562476300/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link |
| Tableau Story | https://public.tableau.com/views/EVMARKET-STORY1/Story1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link |

The Demo Link and GitHub Link are the project's only overall links; the Tableau views are resources used inside it.

## Repository structure

```
dataset/                  ev_market_test.csv (100,000 rows x 37 columns), the single source of truth
analysis/                 validate_dataset.py -> validation_report.md (Parts 1, 2 and expected values)
                          check_published.py + published_capture.json -> published_check.md (Part 6)
                          performance_testing.md (Part 6)
tableau/                  README.md: calculated fields, filters, sheets, dashboard and story spec (Parts 2-5)
ev-market-intelligence/   Flask website that embeds the published dashboard and story (Part 7)
```

## Parts 1–7

| Part | What exists | Where |
| --- | --- | --- |
| 1. Data Collection & Extraction | CSV inspected: 1 table, 100,000 rows, 37 columns, unique `vehicle_id`, 5 columns with nulls. Field map for every project topic. Tableau connection: Text file, one table, extract. | `analysis/validation_report.md` §1–4 |
| 2. Data Preparation | 12 validation checks, all pass; nothing needed deleting or rewriting. Nulls and outliers kept and documented. Calculated fields, Top N parameter and global filters specified with expected values. | `analysis/validation_report.md` §5–7, 10; `tableau/README.md` §2 |
| 3. Data Visualization | The published workbook has 9 worksheets. They cover KPIs, category sales, the map, model-year sales, price vs range, motor power, regional share, manufacturer share and battery degradation. Battery-type distribution, range/capacity and customer rating sheets are specified but **not yet built**. | `tableau/README.md` §3 |
| 4. Dashboard | Published dashboard: 8 worksheets, Automatic size, no filter controls. Layout, theme, filters and actions for the brief are specified. | `tableau/README.md` §4 |
| 5. Story | Published story: 9 points. Revised captions, finding text and recommendations are written, computed from the data. | `tableau/README.md` §5 |
| 6. Performance Testing | Every published sheet compared with pandas (all values match), 10 filter tests (all match), load and interaction times measured. 6 workbook issues found. | `analysis/performance_testing.md`, `analysis/published_check.md` |
| 7. Web Integration | Flask site with home, dashboard and story pages. It embeds the two supplied Tableau Public views and has a footer with the Demo and GitHub links. Tested locally. | `ev-market-intelligence/` |
| 8. Demonstration & Documentation | On hold until its requirements are provided. | — |

## What the data shows

All figures are from `analysis/validation_report.md`:

- Vehicle category drives price, range and battery size: electric buses average $274,045 and 300 kWh,
  two-wheeler scooters $2,531 and 3.3 kWh.
- Two-wheeler scooters sell the most units (85.0M, 11.0%); buses, electric trucks and pickups are 2.4% of units
  but save about 9 t of CO2 a year each, three times a car.
- Solid-state batteries degrade 7.4% in five years and LFP 10.1%, against about 14% for NMC, NCA and sodium-ion.
- The market is fragmented: no manufacturer has more than 0.63% of units.
- Customer ratings average 4.08 out of 5 and barely differ between segments.

## Data notes

- The dataset is synthetic, so findings describe this dataset, not the real EV market.
- There is no sales date. `model_year` (2018–2026) is the only time field, so sales are compared by model year,
  not as calendar-year growth.
- `model_name` repeats across manufacturers; a model is `manufacturer` + `model_name`.
- Price, range, motor power and ratings are per vehicle and must be averaged, not summed.
- CO2 saved per year is the only direct sustainability measure.

## Re-run the analysis

```bash
python -m venv venv
venv\Scripts\python.exe -m pip install -r analysis/requirements.txt
venv\Scripts\python.exe analysis/validate_dataset.py
venv\Scripts\python.exe analysis/check_published.py
```

## Run the website

```bash
venv\Scripts\python.exe -m pip install -r ev-market-intelligence/requirements.txt
venv\Scripts\python.exe ev-market-intelligence/app.py
```

Then open https://ev-market-intteligance.onrender.com The embedded views load from Tableau Public, so the computer needs internet access
and both workbooks must stay public on the Tableau Public profile.
