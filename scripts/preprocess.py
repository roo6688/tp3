"""Préparer les mesures à 100 % SOC après charge sans modifier les originaux.

Sorties : données en format long et bilan des observations exclues.
Aucune interpolation, aucun lissage et aucun retrait automatique d'aberrants.
"""
from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def preprocess(raw=RAW, output=PROCESSED):
    raw, output = Path(raw), Path(output)
    files = sorted(p for p in raw.rglob("*")
                   if p.suffix.lower() in {".csv", ".tab"}
                   and "24h_charge_" in p.name)
    if not files:
        raise FileNotFoundError("Aucun fichier après charge dans data/raw. "
                                "Exécutez d'abord scripts/download_data.py.")
    tables, reports = [], []
    for path in files:
        # Détection du séparateur : CSV original ou fichier tabulé Borealis.
        frame = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
        frame.columns = frame.columns.str.strip()
        if "Timestamp [h]" not in frame.columns:
            raise ValueError(f"Colonne de temps absente : {path.name}")
        columns = [c for c in frame.columns
                   if re.fullmatch(r"BATT_\d+_OCV_V_100-SOC", c)]
        if not columns:
            raise ValueError(f"Aucune colonne à 100 % SOC : {path.name}")
        for column in columns:
            battery = column.split("_OCV")[0]
            table = frame[["Timestamp [h]", column]].copy()
            table.columns = ["time_h", "voltage_V"]
            for name in table.columns:
                table[name] = pd.to_numeric(table[name], errors="coerce")
            table = table.replace([float("inf"), float("-inf")], float("nan"))
            invalid = table.isna().any(axis=1)
            missing_count = int(invalid.sum())
            table = table.loc[~invalid].copy()
            # La période étudiée est explicitement limitée à 0–24 h.
            outside = ~table["time_h"].between(0, 24)
            outside_count = int(outside.sum())
            table = table.loc[~outside].copy()
            # Seuls les doublons strictement identiques peuvent être retirés.
            duplicate_count = int(table.duplicated().sum())
            table = table.drop_duplicates().sort_values("time_h")
            if table.empty:
                raise ValueError(f"Aucune mesure utilisable : {path.name}, {column}")
            if table["time_h"].duplicated().any():
                raise ValueError(f"Tensions contradictoires au même instant : {path.name}")
            table["battery"] = battery
            table["soc_percent"] = 100
            table["condition"] = "after_charge"
            table["source_file"] = path.relative_to(raw).as_posix()
            tables.append(table)
            reports.append({
                "source_file": path.relative_to(raw).as_posix(), "battery": battery,
                "rows_input": len(frame), "invalid_numeric_removed": missing_count,
                "outside_0_24h_removed": outside_count,
                "exact_duplicates_removed": duplicate_count, "rows_output": len(table),
                "min_time_h": table["time_h"].min(), "max_time_h": table["time_h"].max(),
            })
    combined = pd.concat(tables, ignore_index=True)
    if combined.duplicated(["battery", "time_h"]).any():
        raise ValueError("Plusieurs fichiers contiennent la même batterie aux mêmes instants. "
                         "Gardez une seule copie de chaque fichier dans data/raw.")
    combined = combined.sort_values(["battery", "time_h"])
    combined = combined[["battery", "condition", "soc_percent", "time_h",
                         "voltage_V", "source_file"]]
    output.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output / "ocv_charge_100_clean.csv", index=False)
    pd.DataFrame(reports).to_csv(output / "preprocessing_summary.csv", index=False)
    print(f"Traitement terminé : {combined['battery'].nunique()} batteries, "
          f"{len(combined)} observations.")
    print(f"Fichiers enregistrés dans : {output}")
    return combined, pd.DataFrame(reports)


if __name__ == "__main__":
    preprocess()
