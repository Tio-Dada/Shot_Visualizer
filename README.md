# NBA Shot Visualizer & Spatial Analytics Dashboard

An interactive full-stack spatial analytics dashboard built with Python, Streamlit, and Matplotlib. The application queries tracking data from the NBA Stats API, dynamically resolves career metadata across all active and historical playing years, maps deci-foot tracking coordinates to regulation court geometry, and provides dual-engine visualization via individual shot scatter charts and logarithmic hexbin density heatmaps.



## Key Features

* **Dynamic Career Discovery:** Queries the `PlayerCareerStats` endpoint to extract and chronologically sort all regular-season campaigns logged by a given player, eliminating hardcoded season lists.
* **Regulation Vector Court Engine:** Constructs an NBA regulation half-court layout to exact scale using Matplotlib `patches` and line artists anchored to the hoop origin $(0, 0)$.
* **Dual Visualization Engines:**
  * **Shot Outcome Scatter:** Categorizes makes and misses with distinct symbols, high-contrast colors, and alpha transparency to expose shot selection.
  * **Spatial Hexbin Heatmap:** Aggregates coordinate clusters into hexagonal bins with edge blending (`edgecolors='none'`) and logarithmic scaling (`bins='log'`) to counter rim-volume bias.
* **Interactive Slicing & Real-Time KPIs:** Sidebar widgets allow instantaneous filtering by attempt classification (2PT vs. 3PT), dynamically updating Attempts, Makes, and Field Goal Percentage (FG%).
* **Fault-Tolerant & Caching Architecture:** Utilizes Streamlit's `@st.cache_data` to minimize API latency and prevent rate-limiting, backed by defensive validation checks for missing records and misspelled inputs.

---

## Architecture & Data Flow

```text
               [ User Input: Player Name ]
                            │
                            ▼
      data_loader.py: get_player_seasons(pname)
   ┌─────────────────────────────────────────────────┐
   │ • Resolves Player ID via static registry        │
   │ • Fetches PlayerCareerStats                     │
   │ • Returns unique, descending season list        │
   └────────────────────────┬────────────────────────┘
                            │
                            ▼
               [ User Selects Season & Filter ]
                            │
                            ▼
      data_loader.py: get_player_shot_data(...)
   ┌─────────────────────────────────────────────────┐
   │ • Fetches ShotChartDetail (FGA)                 │
   │ • Defensive input validation & null checks      │
   │ • Returns cleaned coordinate DataFrame          │
   └────────────────────────┬────────────────────────┘
                            │
                            ▼
                  app.py (Streamlit UI)
   ┌─────────────────────────────────────────────────┐
   │ • Evaluates KPI metrics (FGA, FGM, FG%)         │
   │ • Handles mode toggle: Scatter vs. Hexbin       │
   │ • Passes Matplotlib axis to court module        │
   └────────────────────────┬────────────────────────┘
                            │
                            ▼
                        court.py
   ┌─────────────────────────────────────────────────┐
   │ • Renders vector geometry in deci-feet units    │
   │ • Sets z-order hierarchy (court lines over data)│
   └────────────────────────┬────────────────────────┘
                            │
                            ▼
               [ Interactive Browser Visual ]