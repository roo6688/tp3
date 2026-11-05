---
Title: Reproducible analysis of OCV relaxation after a full charge
Contributors:
  - Nasma Drissi
  - Ronald Sim
Version: 1.0
---

## Overview

How does the open-circuit voltage (OCV) evolve during 24 hours of rest after a full charge, for the different batteries in the dataset?

To answer it, we use only the after-charge measurements at 100% state of charge (`24h_charge` files, `_100-SOC` columns) for the 8 batteries. For each battery, we compute the voltage change over three periods (0–1 h, 0–24 h and 22–24 h, in mV) and plot the voltage change over time and the total change after 24 h.

The script `download_data.py` retrieves the raw data from the 24-hour raw OCV relaxation dataset for rechargeable batteries with different chemistries in Demo.Borealis, and `preprocess.py` pre-processes the 8 after-charge files. 
The pre-processing step keeps only the 100-SOC columns, converts time and voltage to numeric values, removes missing, non-finite or out-of-range (0–24 h) observations and exact duplicates, and stops if one battery has conflicting voltages at the same time. The result is 11 528 observations for 8 batteries (1 441 per battery). 
For the analysis, `analyze.py` computes three voltage-change indicators per battery (0–1 h, 0–24 h, 22–24 h, in mV) and produces two figures. 
Run `download_data.py`, `preprocess.py`, then `analyze.py`.


## Data Availability and Provenance Statements

- [x] All data used in this project are publicly available.
- [x] The data are **not** redistributed in this repository. They are downloaded automatically by `scripts/download_data.py`.

### Provenance

We did not generate the data. The data comes from the dataset *"24-hour raw OCV relaxation dataset for rechargeable batteries with different chemistries"* (Voicila, Enache, Argyriou, Sarigiannidis, Pisla and Seritan, 2026), which we deposited in Demo.Borealis (Polytechnique Montréal, "Fall 2026" collection). As mentionned in the Borealis README, the files are a subset of the original dataset identified by DOI [10.21227/651q-8v82](https://doi.org/10.21227/651q-8v82).

The data record the open-circuit voltage (OCV) of rechargeable batteries during 24 hours of rest after a charge or discharge procedure, with one measurement per minute (1 441 observations per curve). For the measurement protocol, instruments, and battery characteristics, refer to the original dataset's documentation.

### Data source and access

| Item | Details |
|---|---|
| Dataset | 24-hour raw OCV relaxation dataset for rechargeable batteries with different chemistries |
| Version used | 2.0 |
| Location | [Demo.Borealis, doi:10.80240/FK2/WRCLHO](https://demo.borealisdata.ca/dataset.xhtml?persistentId=doi:10.80240/FK2/WRCLHO&version=2.0) |
| Original dataset | [doi:10.21227/651q-8v82](https://doi.org/10.21227/651q-8v82) |
| Access | Open (no account needed to download) |
| License / reuse terms | CC-BY 4.0 |
| Files used | The eight "after charge" files (`24h_charge`), 100-SOC columns only |
| Retrieved | 2026-10-27 |


### Data files and variables used

| Variable | Description | Unit |
|---|---|---|
| `Timestamp [h]` | Time elapsed since the start of rest | hours |
| `BATT_<n>_OCV_V_100-SOC` | Open-circuit voltage of battery `BATT_<n>` after a full charge (one column per battery) | volts |

Only measurements at 100% state of charge after a charge procedure are used. Discharge files and other SOC levels are not analyzed.

### Details on each Data Source

- **Format:** `.tab` (tab-separated), as downloaded by `download_data.py`.
- **Data dictionary:** The `README.md` published with the Borealis dataset describes the columns. Variables used: `Timestamp [h]` (hours) and the voltage columns `BATT_<n>_OCV_V_100-SOC` (volts), one per battery.
- **How we obtained the data:** From Demo.Borealis (see the table above), using `scripts/download_data.py`.
- **How others can obtain them:** Run `python scripts/download_data.py`, or download the files manually from the Demo.Borealis page (see the table above).

### Rights and license

The authors of this repository have legitimate access to and permission to use the data (publicly available on Borealis under CC-BY 4.0). The data are not redistributed here.

 `download_data.py` downloads them directly from Borealis. Anyone reusing the data should follow the CC-BY 4.0 terms and cite the dataset (see References). The `LICENSE` file in this repository covers the code only.

## Repository Structure
```
tp3/
├── .github/workflows/
│   └── check-files.yml
├── data/                            # Created by the scripts, not tracked by Git
│   ├── raw/                         # Files downloaded by download_data.py
│   └── processed/                   # Output of preprocess.py  
├── figures/                         # Already in repo / Created by analyze.py
│   ├── ocv_relaxation_curves.png    
│   └── ocv_variation_24h.png
├── results/                         # Created by analyze.py (ocv_indicators.csv)
├── scripts/
│   ├── download_data.py    
│   ├── preprocess.py       
│   └── analyze.py
├── .gitignore
├── AI_Prompts.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE 
├── README.md
├── report.md
└── requirements.txt
```

## Requirements

- [x] The repository contains a `requirements.txt` listing all Python dependencies. 
- Python 3.11.8
  - `pandas` 2.2.3
  - `numpy` 2.4.6
  - `matplotlib` 3.11.2

- Steps for installing these dependencies are included in the [instructions to replicators](#instructions-to-replicators).

## Instructions to Replicators

1. Clone the repository and open a terminal in its root folder.

   `git clone https://github.com/roo6688/tp3.git`

   `cd tp3`
2. Create the environment:

   Windows PowerShell: `python -m venv .venv`, then `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
   
   macOS/Linux: `python3 -m venv .venv`, then `.venv/bin/python -m pip install -r requirements.txt`.
   
3. Download the data:

   `.\.venv\Scripts\python.exe scripts/download_data.py`
4. Preprocess: 
   
   `.\.venv\Scripts\python.exe scripts/preprocess.py`
   
   Expected message: Traitement terminé : 8 batteries, 11528 observations.
5. Analyze: 

   `.\.venv\Scripts\python.exe scripts/analyze.py`
   
   Expected message: Analyse terminée : 8 batteries.
6. Find the outputs in `data/processed/`, `results/` and `figures/`.

Run the scripts in this order. If `data/raw/` already contains the files, skip step 3.

## Files downloaded and produced

| File | Created by | Description |
|---|---|---|
| `data/raw/ocv_relaxation_24h__24h_charge_<label>.tab` (8 files; labels `apr`, `ar`, `au`, `bse`, `lg`, `li`, `oem`, `sg`) | `download_data.py` | Raw 24 h rest voltage curves after charge, downloaded from Borealis (v2.0), tab-separated. Contains `Timestamp [h]` and `BATT_<n>_OCV_V_<SOC>` voltage columns. |
| `data/processed/ocv_charge_100_clean.csv` | `preprocess.py` | Clean long-format table of the 100-SOC measurements: 8 batteries, 11 528 rows. Columns: `battery`, `condition` (`after_charge`), `soc_percent` (100), `time_h` (h), `voltage_V` (V), `source_file`. |
| `data/processed/preprocessing_summary.csv` | `preprocess.py` | One row per battery curve: `source_file`, `battery`, `rows_input`, `invalid_numeric_removed`, `outside_0_24h_removed`, `exact_duplicates_removed`, `rows_output`, `min_time_h`, `max_time_h`. |
| `results/ocv_indicators.csv` | `analyze.py` | One row per battery: `n_observations`, voltages at 0, 1, 22 and 24 h (`V_0h_V`, `V_1h_V`, `V_22h_V`, `V_24h_V`), and signed changes in mV (`delta_V_0_1h_mV`, `delta_V_0_24h_mV`, `delta_V_22_24h_mV`). Negative = voltage drop. |
| `figures/ocv_relaxation_curves.png` | `analyze.py` | Line plot of V(t) − V(0) in mV over 24 h of rest, one curve per battery. |
| `figures/ocv_variation_24h.png` | `analyze.py` | Bar chart of V(24 h) − V(0) in mV for each battery. |

## Description of programs/code

- `scripts/download_data.py` downloads the eight after-charge files from Borealis into `data/raw/`.
- `scripts/preprocess.py` selects the 100-SOC columns, converts time and voltage to numbers, removes missing, non-finite or out-of-range (outside 0–24 h) observations and exact duplicates, and stops if one battery has conflicting voltages at the same time. It writes the two files in `data/processed/`.
- `scripts/analyze.py` computes three indicators per battery (voltage change over 0–1 h, 0–24 h and 22–24 h, in mV) and saves two figures.
- `report.md` presents the question, method, results and limitations.

Scripts determine paths from their own location, so they must stay in `scripts/` and can be run from the project root.

## License

The code is licensed under the MIT license. See the `LICENSE` file for details.

## References

Iulian-Teodor Voicila, Bogdan-Adrian Enache, Irina Vilciu, George-Calin Seritan, "24-hour raw OCV relaxation dataset for rechargeable batteries with different chemistries", IEEE Dataport, May 22, 2026, doi:10.21227/651q-8v82

Voicila, Teodor-Iulian; Enache, Bogdan-Adrian; Argyriou, Vasilis; Sarigiannidis, Panagiotis; Pisla, Mihai-Alexandru; Seritan, George-Calin, 2026, "24-hour raw OCV relaxation dataset for rechargeable batteries with different chemistries", https://doi.org/10.80240/FK2/WRCLHO, Borealis, V2, UNF:6:LbmBU2xKUWLNPvxSc5YvHA== [fileUNF] 


## Acknowledgements

Structure adapted from the [social science data editors' README template](https://social-science-data-editors.github.io/template_README/).
