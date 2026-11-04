# geomind app: list of bugs and tasks (2 November, 21:15)

## ✓ Done (testable on localhost:5173)
- Saving a template plant, study progress and cancel, theme, logo, icons, Case name
- Case form:
  - Rewrite of the form engine
  - Inline series picker with upload and a chart with axes
  - Removed the Files tab and replaced it with a Files button
  - Mole percent table for gas composition
  - Requirements cards
  - Uncertainty label
  - Removed Range from Case
  - Fixed the red economics error
- Flowsheet editor:
  - Left-to-right layout with groups
  - Categorized palette
  - Templates window
- Results:
  - Constraints table with limit and distance to limit
  - KPIs in three groups
  - Sensitivity and Uncertainty table
  - "Take this design as a plant"
  - Daily coverage for old results
- Chat: "What it knows", unit status, tool summary, ⋯ menu in the list, incomplete Case notice
- Report: sections, KPI, flowsheet image, coverage and demand/supply charts, Compact button (‏PDF 5 and 2 pages)
- The MinIO bucket is created at startup (500 error when deleting a project)
- The Operation section was hidden
- Live test (c): stopping at a 0.01 dollar cap worked correctly
- Live test (a): save_profile with the real model succeeded (0.34 dollars, 36 seconds); the "event loop" error at the budget cap was fixed
- The main server (geomind.team) was rebuilt with these same versions: backend d9cc113, frontend 54ec994, gemini 0.5.3, geomind 0.4.1 (2 November 21:35)
- The competition project reads with hackathon.py: ‏LCTS 40.34, ‏CO2 12.90 kt, sensitivity, uncertainty, coverage 365 days
- Number checks: gas balance, CO2, electricity, CAPEX, and COP 14.6 (per the model's rule)

## ✱ In progress
- Report:
  - Dark theme on screen (it is too light now)
  - Flowsheet without scrolling and readable
  - Pipes outside the capacity table
  - Readable module names
- Numeric question: "geothermal 365 days" for cooling that comes from the electric chiller; do the 112 heating backup days also include the 35 shutdown days?
- Compare:
  - Show only the designs (not Sensitivity and Uncertainty)
  - Overlapping labels
  - LCTS axis
  - Doublet, depth and CAPEX columns
- Connecting gemini 0.5.3:
  - Full list of gaps
  - Units, limits and percent from the schema
  - Minimize objectives
  - Explanation of study types
  - Display units
  - Separating warnings from errors (important change)

## ○ Next
- Live test (b): with a 0.5 dollar cap it stopped before running the study; a rerun waits for approval of a larger cap
- Readable message for a budget stop (it now shows a raw ID and number)
- "Add to Case" button after save_profile
- Chat: final answer as a message (not a cut-off finish row); Python text in the tool row
- Quantity filter by section in Requirements (gm.plants.roles())
- Readable error for a study on an empty Case
- Full review of the look on desktop 1920 and mobile 390, empty Overview page
- JSON coloring and chart zoom (low priority)
- Delivery guide and final report

## Waiting on gemini
- 2.7% (‏580 MWh) difference in the gas makeup balance, asked
- Wrong total count in on_progress (progress bar over 100%)
- COP 14.6 is physically optimistic (if you want, it is logged as a modeling question)

## Waiting on geomind
- set_case for the analyst agent (incomplete Case)
- save_profile sends the unit 'day' instead of 'd'
- The update_state schema is unclear (3 failed attempts)
- High cost: 190 thousand input tokens for a simple save
- size_plant: the argument shape (design/<name>) and the missing size.doublets.range ate most of the budget of test (b)
- It did not use the project's plant and built a new plant
- After a budget stop it gives the user no partial answer
- The budget is checked before each call, so one call goes over the cap
- hook docs: UsageLedger.spent runs on the event loop, not the worker thread

## Waiting on you
- Default flowsheet zoom: readable (my suggestion) or the whole plant
