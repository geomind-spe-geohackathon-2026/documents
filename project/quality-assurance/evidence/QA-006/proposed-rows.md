# QA-006: proposed catalogue rows (waiting for Sahand's approval)

Option A (Sahand): cited rows for the economics keys the question left open. Nothing is in the
catalogue (`geomind/data/knowledge/cost-sources.csv`) or Knowledge yet. The rows, in the
catalogue's columns, are in [proposed-rows.csv](proposed-rows.csv). Conversion as in
`cost-sources.md`: EUR at 2015 prices by Eurostat HICP (euro area, 2015 = 100); the factors are
the ones the catalogue's other rows already use.

| Key | Proposed value_2015 | Source | Notes |
|---|---|---|---|
| `opex.fixed.compression_chiller` | **4639.7 EUR/MW/yr** (recommended) | Heat Roadmap Europe D3.2 (Mines ParisTech, 2017), p.42: water-cooled chiller > 400 kW, 755 kW, fixed O&M 3503 EUR/unit/yr | 2015 column read as 2015 prices. |
| | 4309 EUR/MW/yr (other row) | Tri-County Technical College district chilled water study (2013), p.2: "$ 20 per ton per year for maintenance for district chiller plant" | USD 2013 at the ECB 2013 average 1.3281 USD/EUR (check), HICP x1.00624. |
| `opex.fixed.absorption_chiller` (extra) | 6800 EUR/MW/yr | HRE4 D3.2, p.49: Water-LiBr absorption chiller, 500 kW, fixed O&M 3400 EUR/unit/yr | Replaces a placeholder row. |
| `opex.fixed.production_pump` | **20 %/yr** of the ESP capex | ECN-O--12-043 (Straathof, 2012), p.29: ESP replaced every five years (DoubletCalc default) | Assumes one workover costs about one ESP. EBN's 2025 ESP workshop gives 1-2 year run times in NL (50-100 %/yr): 20 % is the low end. |
| `opex.per_energy.compression_chiller`, `.absorption_chiller`, `.adsorption_chiller` | **no row** | HRE4 D3.2 gives chiller O&M as fixed only ("all costs that are independent of how the unit is operated ... reinvestments ... included"); no source found with a variable O&M per MWh of cold apart from the electricity or heat that drives it | Proposal: leave open, or set 0 EUR/MWh with the note "O&M counted in opex.fixed (HRE4 D3.2)"; Sahand decides. |
| `revenue.subsidy.capacity` | **no row** | Not a price: the MW a subsidy decision grants (SDE++ caps full-load hours per MW), so it is project-specific | Proposal: the user gives it, or the design's geothermal capacity; no catalogue row. |
| `opex.fixed.adsorption_chiller` | no row | No source found | Stays open. |

To add after approval: append the approved rows to `geomind/data/knowledge/cost-sources.csv`
(and gemini's `docs/cost-sources/sources.csv` if wanted), note them in `cost-sources.md`, release
geomind, and re-seed Knowledge on production (`python -m scripts.knowledge` in the backend).

Searched but not usable: DEA technology data (no chiller sheet found), TNO/EBN ESP figures without
amounts, per-ton figures from Hong Kong and Jakarta studies.
