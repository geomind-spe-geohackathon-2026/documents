# Benchmark plan: GEMINI (refactor branch) vs open-source geothermal tools

Status 2026-10-28: plan only, waiting for the new repo (proposed `swarmax/geothermal-benchmark`, private).

## Tools to compare (all installable in this environment)
| Tool | Scope | Install |
|---|---|---|
| GEMINI (`refactor` branch) | doublet equipment modules (ESP, wells, reservoir, HX, boiler, degasser, filter), engine (simulate / replay / live), calibration, legacy bridge, agent (planned) | git clone fork |
| GEOPHIRES-X (NREL) | reservoir + wellbore + surface plant + economics (LCOH, NPV), direct-use heat, heat pump, absorption chiller, district heating | `pip install git+https://github.com/NREL/GEOPHIRES-X` |
| pyThermoGIS / DoubletCalc (TNO) | doublet power, flow, COP, LCOE, probabilistic (P10/P50/P90) | `pip install pythermogis` (0.1.6) |
| TESPy | thermodynamic plant design (HX, heat pump, pumps), off-design | `pip install tespy` (0.11.3) |
| pandapipes | district heating pipe network hydraulics + heat losses | `pip install pandapipes` (0.16.0) |
| oemof.solph | energy-system dispatch / sizing optimisation (MILP) | `pip install oemof.solph` (0.6.5) |

## Part 1: feature table
Rows: reservoir/IPR, wellbore dP/dT, ESP, HX, heat pump, absorption chiller, storage, network,
economics, uncertainty, optimisation/calibration, time-series replay of measured data,
live/digital-twin, corrosion/erosion/scaling, agent/LLM interface, API style.
Each cell: yes / partial / no + link to source line or doc.

## Part 2: one shared doublet case (from GEMINI example data)
80 °C reservoir, 220 bar, top 1800 m, PI 21 / II 20 m3/h/bar, 150 m3/h, reinjection 20 °C (~10.9 MW).
Same inputs in every tool via one `case.yaml` and one adapter per tool.
Compared outputs: thermal power, ESP/pump power, wellhead T and p, COP, (where available) LCOH.
Then a 2nd case once task inputs arrive (2026-10-29): heating + cooling demand.

## Repo layout (proposal)
```
cases/doublet_base.yaml
adapters/{gemini,geophires,thermogis,tespy}.py   # case -> tool input -> common result dict
run_all.py  -> results/doublet_base.csv
report/comparison.md (feature table + numbers + differences explained)
tests/ (fast smoke test per adapter)
```
