# Tableau workbook guide (Parts 1–5)

This is the reference for the Tableau side of the project. It records what the published workbooks contain
(read through the Tableau Embedding API on 2026-10-29, see `analysis/published_check.md`). It also specifies the
calculated fields, filters, sheets, dashboard layout and story changes needed to meet the project brief. Every
expected value comes from `analysis/validation_report.md`.

| Published view | Workbook on Tableau Public | Contents |
| --- | --- | --- |
| [Dashboard](https://public.tableau.com/views/EVMARKET-STORY_17932562476300/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) | EV MARKET - STORY | `Dashboard 1`, 8 worksheets, size Automatic |
| [Story](https://public.tableau.com/views/EVMARKET-STORY1/Story1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) | EV MARKET - STORY 1 | `Story 1`, 9 story points, one worksheet each |

The dashboard and story are in **two separate workbooks**, so every change below has to be made in both
(the story workbook has the same 8 worksheets plus `Battery Degradation Matrix`). No `.twbx` is saved in this
repository yet; see [Save a copy](#7-save-a-copy-and-republish).

## 1. Connect the data (Part 1)

1. Tableau Public > **Connect > To a File > Text file** > `dataset/ev_market_test.csv`.
2. One table, so no joins or relationships are needed.
3. Check that Tableau reads 37 fields and, after the extract is built, 100,000 rows (status bar or
   `SUM([Number of Records])`). Tableau Public stores published data as an **Extract** (Hyper), which also keeps
   interaction fast with 100,000 rows.

## 2. Prepare the fields (Part 2)

The CSV needs no cleaning: no duplicates, no label variants, no impossible values
(`analysis/validation_report.md` section 5). Nulls are kept; Tableau's `AVG` and `SUM` skip them.

**Field settings in the Data pane**

| Field | Change | Why |
| --- | --- | --- |
| `model_year` | Convert to **Dimension**, **Discrete** | Stops Tableau from summing years |
| `manufacturing_country` | **Geographic Role > Country/Region** | Enables the map (all 10 countries geocode, including UK and USA) |
| `vehicle_id` | Keep as Dimension | Unique ID for counting vehicles |
| `price_usd`, `range_km`, `battery_capacity_kwh`, `motor_power_kw`, `torque_nm`, `efficiency_wh_per_km`, `customer_rating`, `safety_rating_stars`, `battery_degradation_pct_5yr`, `battery_cycle_life` | **Default Properties > Aggregation > Average** | These are per-vehicle values; adding them up is meaningless (this is what went wrong in the Top Models sheet) |
| `annual_sales_units`, `co2_saved_tons_per_year` | Keep **Sum** | Additive totals |

**Calculated fields**

Create these with **Analysis > Create Calculated Field**. All of them are needed by the sheets below.

| Name | Formula | Format | Expected (no filters) |
| --- | --- | --- | --- |
| Total EV Sales | `SUM([annual_sales_units])` | Number, millions, 1 dp | 772.6M |
| Average Driving Range | `AVG([range_km])` | Number, 0 dp, suffix " km" | 324 km |
| Average Battery Capacity | `AVG([battery_capacity_kwh])` | Number, 1 dp, suffix " kWh" | 78.2 kWh |
| Average Customer Rating | `AVG([customer_rating])` | Number, 2 dp | 4.08 |
| EV Count | `COUNTD([vehicle_id])` | Number | 100,000 |
| Model | `[manufacturer] + " " + [model_name]` | — | 98,571 distinct |
| Market Share | `SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))` | Percentage, 2 dp | SurgeWorks 0.63% |
| Top N Manufacturers | `RANK(SUM([annual_sales_units]), 'desc') <= [Top N]` | Boolean filter (keep True) | 10 bars, 46,691,869 units |
| Model-Year Sales Change | `(SUM([annual_sales_units]) - LOOKUP(SUM([annual_sales_units]), -1)) / ABS(LOOKUP(SUM([annual_sales_units]), -1))` | Percentage, 1 dp | 2019: +2.96% |
| Price Band | `IF [price_usd] < 10000 THEN "Under $10k" ELSEIF [price_usd] < 30000 THEN "$10k-30k" ELSEIF [price_usd] < 60000 THEN "$30k-60k" ELSEIF [price_usd] < 100000 THEN "$60k-100k" ELSE "$100k+" END` | — | 5 bands, see report section 10 |
| Total CO2 Saved | `SUM([co2_saved_tons_per_year])` | Number, thousands | 368,946 t / year |

Notes on the calculations:

- **Market Share** and **Top N Manufacturers** are table calculations. Set both to *Compute Using >
  manufacturer*. Because the Top N filter is a table calculation, it only hides bars and does not change the
  denominator. Each manufacturer's share therefore stays a share of all filtered sales, not of the bars shown.
- **Model-Year Sales Change** compares model-year cohorts. There is no sales date, so do not label it
  "growth" or "YoY sales". The first year has no previous value and shows blank.
- Zero denominators cannot occur: total sales is never zero for any filter combination that returns rows.

**Parameter**

| Name | Type | Values | Default |
| --- | --- | --- | --- |
| Top N | Integer, Range | 1 to 50, step 1 | 10 |

Right-click it > **Show Parameter** on the dashboard.

**Filters (global)**

Add each to one sheet, then **Apply to Worksheets > All Using This Data Source**, and show it on the dashboard:

| Filter | Control | Notes |
| --- | --- | --- |
| category | Multiple values (dropdown) | 15 values |
| manufacturing_country | Multiple values (dropdown) | 10 values |
| market_region | Multiple values (dropdown) | 7 values |
| battery_type | Multiple values (list) | 5 values |
| model_year | Multiple values (dropdown) | 2018 to 2026 |
| Price Band | Multiple values (list) | 5 bands |
| manufacturer | Multiple values (search) | 200 values; optional |

If any sheet keeps a dimension **Top** filter (Filter > Top tab), right-click the global filters > **Add to Context**.
Otherwise the Top filter is computed before them and ignores them. That is how the published Manufacturer Market
Share chart behaves today: with Model Year = 2024 it still shows the overall top 14, of which only 5 are in the
2024 top 14.

## 3. Visualizations (Part 3)

**Coverage of the brief by the published sheets**

| # | Brief | Published sheet | Status | Action |
| --- | --- | --- | --- | --- |
| 1 | KPI summary | Top Summary KPIs (sales, motor power, price, range, safety) | Values correct | Make the tile taller (numbers are cut off at small sizes) |
| 2 | Sales by vehicle category | Sales By Category (bar) | **Shows 11 of 15 categories** | Clear the Category filter |
| 3 | Manufacturer ranking | Manufacturer Market Share (treemap) | Top 14 by units; no share shown | Use Top N + Market Share (sheet spec below) |
| 4 | Battery technology distribution | — (story has Battery Degradation Matrix) | Missing on dashboard | Add **Battery Technology** sheet |
| 5 | Driving range comparison | — (range only appears in Price vs Range) | Missing | Add **Range and Battery by Category** sheet |
| 6 | Battery capacity analysis | — | Missing | Same new sheet as #5 |
| 7 | Manufacturing country distribution | Global EV Map (filled map) | Correct | Keep |
| 8 | Customer satisfaction | — (KPI uses safety stars, not customer rating) | Missing | Add **Customer Rating by Category** sheet |
| 9 | Price vs performance | Price vs Range (scatter, 100,000 marks) | Correct | Keep; lower mark size/opacity |
| — | (extra) | Sales Trend by Year (line by region) | Correct values | Rename "Sales by Model Year" |
| — | (extra) | Top Models by Horsepower / Motor Power (packed bubbles) | **Sizes are SUM of kW** | Change to MAX, label by Model |
| — | (extra) | Market Share by Region (pie) | **2 of 21 slices excluded** | Remove the exclusion |

**Specs for the sheets to add or fix**

| Sheet | Columns / Rows | Marks | Sort, labels, tooltip | Expected values |
| --- | --- | --- | --- | --- |
| Sales By Category (fix) | Rows `category`; Columns `Total EV Sales` | Bar | Sort descending; label in millions; tooltip adds EV Count and Market Share | 15 bars; Two-Wheeler Scooter 85.0M, Electric Bus 5.3M |
| Manufacturer Ranking (fix) | Rows `manufacturer`; Columns `Total EV Sales`; Filter `Top N Manufacturers` = True | Bar | Sort descending; label `Market Share` | Top 10: SurgeWorks 4,883,639 (0.63%) … ZapWorks 4,532,114 |
| Battery Technology (new) | Rows `battery_type`; Columns `EV Count`; Color `battery_type` | Bar | Label percent of total; tooltip AVG degradation and cycle life | NMC 33,836 (33.8%), LFP 32,101, NCA 17,234, Sodium-Ion 9,836, Solid-State 6,993 |
| Range and Battery by Category (new) | Rows `category`; Columns `Average Driving Range` and `Average Battery Capacity` (side by side) | Bar | Sort by range; labels with units | Luxury Sedan 549 km / 89.9 kWh; Two-Wheeler 105 km / 3.3 kWh |
| Customer Rating by Category (new) | Rows `category`; Columns `Average Customer Rating`; reference line = overall average | Circle (dot plot) | Axis 4.05 to 4.12 with a note that the spread is only 0.02; tooltip `COUNT([customer_rating])` | Crossover 4.095 highest, Electric Truck 4.074 lowest, overall 4.085 |
| Top Models by Motor Power (fix) | Text/size `MAX([motor_power_kw])` by `Model` | Bar or packed bubbles | Filter Top 15 by MAX power | All 15 between 748.6 and 750.0 kW |
| Market Share by Region (fix) | `market_region` × `drivetrain`, `Market Share` | Pie or stacked bar | Remove the exclusion filter | 21 slices summing to 100% |

## 4. Dashboard (Part 4)

Current state: title "EV Market Performance & Insights", 8 worksheets in a tiled layout with size **Automatic**,
one colour legend, **no filter controls and no parameters**. At 674 × 720 px (the website on a laptop-sized
window) the KPI numbers are cut off.

Changes:

1. **Size:** Dashboard > Size > **Fixed size 1200 × 1100** (or Range, min 1000 × 900). With a fixed size the KPI
   row keeps its height and the website shows the whole layout with a scrollbar on small screens.
2. **Title:** "Electric Vehicle Market Intelligence Dashboard", sans-serif (Tableau Book / Bold), white on dark
   navy `#0B1F33`, matching the website.
3. **Theme:** navy `#0B1F33` header, white background, green `#22C55E` accents; one sequential green palette for
   measures and Tableau 10 for categories.
4. **Layout** (tiled, top to bottom):
   - Title bar, then KPI row (Total EV Sales, Average Driving Range, Average Battery Capacity, Average Customer
     Rating, plus the existing price and motor power if space allows), then the filter row (Category, Country,
     Region, Battery Type, Model Year, Price Band, Top N).
   - Row 1: Sales By Category | Manufacturer Ranking (Top N).
   - Row 2: Battery Technology | Range and Battery by Category.
   - Row 3: Global EV Map | Customer Rating by Category.
   - Row 4: Price vs Range | Sales by Model Year.
5. **Interactivity:** filters apply to all sheets from this data source; add **Dashboard > Actions > Filter**
   (Select, source Global EV Map and Sales By Category, targets all other sheets) so a click on a country or
   category filters the rest.
6. **Tooltips:** show the measure with its unit and EV Count on every sheet.

## 5. Story (Part 5)

Current story points (all with a caption and one worksheet; the story opens on point 2 because it was saved with
that point selected):

| # | Current caption | Sheet |
| --- | --- | --- |
| 1 | Global Overview: KPIs & Performance | Top Summary KPIs |
| 2 | Geographic Distribution: Global EV Map | Global EV Map |
| 3 | Sales Growth: Annual Trend Analysis | Sales Trend by Year |
| 4 | Category Analysis: Vehicle Type Sales | Sales By Category |
| 5 | Pricing Strategy: Price vs Driving Range | Price vs Range |
| 6 | Market Leaders: Top Models & Power | Top Models by Horsepower / Motor Power |
| 7 | Battery Tech: Battery Degradation Matrix | Battery Degradation Matrix |
| 8 | Market Share: Manufacturer Breakdown | Manufacturer Market Share |
| 9 | Regional Market Share: Global Distribution | Market Share by Region |

Proposed nine scenes, following the brief and reusing the fixed and new sheets. Each finding is computed from
the data and is meant to go in a text box on that story point:

| # | Caption | Sheet | Finding text |
| --- | --- | --- | --- |
| 1 | EV Market Overview | Top Summary KPIs | 100,000 vehicle records from 200 manufacturers: 772.6M annual sales units across the 2018–2026 model years, 324 km average range, $65,010 average price. |
| 2 | Vehicle Categories | Sales By Category | Two-wheeler scooters sell the most units (85.0M, 11.0%). Buses, electric trucks and pickups together are 2.4% of units. |
| 3 | Manufacturer Performance | Manufacturer Ranking | The market is fragmented: SurgeWorks leads with 0.63% of units and the top 10 together hold 6.0%. |
| 4 | Battery Technology | Battery Technology + Battery Degradation Matrix | NMC (33.8%) and LFP (32.1%) lead. Solid-state packs lose 7.4% in five years and LFP 10.1%, against about 14% for the rest. The mix does not change across model years. |
| 5 | Driving Range | Range and Battery by Category | Luxury sedans (549 km) and luxury SUVs (525 km) go furthest; scooters average 105 km. |
| 6 | Battery Capacity and Range | Range and Battery by Category | Size of pack is not everything: buses carry 300 kWh for 270 km, luxury sedans 90 kWh for 549 km. |
| 7 | Manufacturing Geography | Global EV Map | All 10 countries are within 4.4% of each other; China builds the most units (78.9M), France the fewest (75.6M). |
| 8 | Customer Satisfaction | Customer Rating by Category | Ratings average 4.08 out of 5 and differ by only 0.02 between categories, so they do not separate segments. |
| 9 | Price, Performance and Recommendations | Price vs Range | Price follows battery capacity (r = 0.84) far more than range (r = 0.28). See the recommendations below. |

Evidence-based recommendations for scene 9:

- **Volume:** the biggest unit segments are two-wheeler scooters, sedans, compact SUVs and hatchbacks (together 40.8% of units).
- **Durability positioning:** LFP (about 2,500 cycles) and solid-state (about 3,000 cycles) last longer than NMC,
  NCA and sodium-ion (about 1,600–1,800). That suits fleet and commercial use.
- **Sustainability research:** each bus, electric truck or pickup saves about 9 t of CO2 a year, three times a car.
  Fleet electrification gives the largest saving per vehicle.
- **Pricing:** in this data, price tracks pack size rather than range, so efficiency (km per kWh) is the lever for
  offering more range without a higher price.

Also: rename the story title "Story 1" to "The EV Market Story", and select point 1 before saving so the story
opens on the overview.

Do not add claims about market growth or technology adoption over time. The data has model years but no sales
dates, and sales and battery mix are flat across model years.

## 6. Fix checklist

In order of impact; make each change in both workbooks.

- [ ] Sales By Category: clear the Category filter (34.4% of units are hidden).
- [ ] Market Share by Region: remove the exclusion of FWD / South Asia and RWD / Latin America (shares are
      overstated by about 11%).
- [ ] Top Models by Motor Power: change SUM to MAX of `motor_power_kw` and show `Model` (manufacturer + name).
- [ ] Manufacturer Market Share: switch to Top N parameter + Market Share, or add global filters to context.
- [ ] Set default aggregation to Average for per-vehicle measures (section 2).
- [ ] Add the calculated fields, Top N parameter and global filters (section 2).
- [ ] Add Battery Technology, Range and Battery by Category, and Customer Rating by Category (section 3).
- [ ] Dashboard: fixed size, new title and theme, filter row, filter actions (section 4).
- [ ] Story: captions, finding text, title, open on point 1; rename "Sales Growth" (section 5).

After the changes, run the filter tests in `analysis/validation_report.md` section 10 and compare.

## 7. Save a copy and republish

1. **File > Save As** > `tableau/EV_Market_Intelligence.twbx` in this repository (packaged workbook with the
   extract), so the project has the workbook file.
2. **File > Save to Tableau Public** from the same workbook overwrites the published view. Check afterwards that
   the URL has not changed. If it has, update `TABLEAU_DASHBOARD_URL` / `TABLEAU_STORY_URL` in
   `ev-market-intelligence/config.py`.
3. Re-run the capture (`analysis/published_capture.json`) and `python analysis/check_published.py`.
