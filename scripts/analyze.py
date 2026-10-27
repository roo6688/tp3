"""Calculer trois variations de tension et produire deux figures.

Entrée : data/processed/ocv_charge_100_clean.csv (issu de preprocess.py).
Les indicateurs utilisent les mesures à 0, 1, 22 et 24 heures, sans interpolation.
Les variations sont signées et exprimées en millivolts.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib

# Enregistrer les graphiques fonctionne aussi sans fenêtre graphique.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "ocv_charge_100_clean.csv"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def voltage_at(table, hour, battery):
    # Tolérance limitée aux arrondis de représentation du temps.
    selected = table.loc[np.isclose(table["time_h"], hour, rtol=0, atol=1e-8),
                         "voltage_V"]
    if len(selected) != 1:
        raise ValueError(f"{battery} : une mesure unique est requise à {hour} h "
                         f"({len(selected)} trouvée(s)). Vérifiez les données.")
    return float(selected.iloc[0])


def main():
    if not INPUT.exists():
        raise FileNotFoundError("Données préparées introuvables. "
                                "Exécutez d'abord python scripts/preprocess.py.")
    data = pd.read_csv(INPUT)
    required = {"battery", "condition", "soc_percent", "time_h", "voltage_V"}
    if not required.issubset(data.columns):
        raise ValueError(f"Colonnes manquantes : {required - set(data.columns)}")
    if data.empty or data[list(required)].isna().any().any():
        raise ValueError("Tableau vide ou valeurs manquantes dans les colonnes requises.")
    if not np.isfinite(data[["time_h", "voltage_V"]].to_numpy(dtype=float)).all():
        raise ValueError("Le temps et la tension doivent être des nombres finis.")
    if not (data["soc_percent"].eq(100) & data["condition"].eq("after_charge")).all():
        raise ValueError("L'analyse attend uniquement les mesures après charge à 100 % SOC.")
    if not data["time_h"].between(0, 24).all():
        raise ValueError("Les temps doivent être compris entre 0 et 24 h.")
    if data.duplicated(["battery", "time_h"]).any():
        raise ValueError("Plusieurs observations pour une même batterie au même instant.")

    summaries, curves = [], []
    for battery, table in data.groupby("battery", sort=True):
        table = table.sort_values("time_h").copy()
        v0, v1, v22, v24 = [voltage_at(table, h, battery) for h in (0, 1, 22, 24)]
        summaries.append({"battery": battery, "n_observations": len(table),
                          "V_0h_V": v0, "V_1h_V": v1,
                          "V_22h_V": v22, "V_24h_V": v24,
                          "delta_V_0_1h_mV": 1000 * (v1 - v0),
                          "delta_V_0_24h_mV": 1000 * (v24 - v0),
                          "delta_V_22_24h_mV": 1000 * (v24 - v22)})
        # Soustraire la tension initiale permet de comparer les changements.
        table["delta_voltage_mV"] = 1000 * (table["voltage_V"] - v0)
        curves.append(table)

    summary = pd.DataFrame(summaries)
    for folder in (RESULTS, FIGURES):
        folder.mkdir(parents=True, exist_ok=True)
    summary.to_csv(RESULTS / "ocv_indicators.csv", index=False, float_format="%.6f")
    colors = plt.get_cmap("tab10").colors
    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    for i, table in enumerate(curves):
        ax.plot(table["time_h"], table["delta_voltage_mV"],
                label=table["battery"].iloc[0], color=colors[i % len(colors)], lw=1.7)
    ax.set(xlabel="Temps de repos (h)", ylabel="Variation de tension V(t) − V(0) (mV)",
           title="Relaxation de la tension après charge complète", xlim=(0, 24))
    ax.axhline(0, color="black", lw=0.7)
    ax.grid(alpha=0.25)
    ax.legend(title="Batterie", ncol=2)
    fig.savefig(FIGURES / "ocv_relaxation_curves.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    bars = ax.bar(summary["battery"], summary["delta_V_0_24h_mV"],
                  color=[colors[i % len(colors)] for i in range(len(summary))])
    ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=9)
    ax.set(xlabel="Batterie", ylabel="Variation de tension V(24 h) − V(0) (mV)",
           title="Variation totale après 24 heures de repos — après charge complète")
    ax.axhline(0, color="black", lw=0.7)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.margins(y=0.18)
    fig.savefig(FIGURES / "ocv_variation_24h.png", dpi=200)
    plt.close(fig)
    print(f"Analyse terminée : {len(summary)} batteries.")
    print("Tableau : results/ocv_indicators.csv")
    print("Graphiques : figures/ocv_relaxation_curves.png et figures/ocv_variation_24h.png")
    print("Variations négatives = baisse de tension. "
          "La variation sur 22–24 h ne prouve pas à elle seule l'équilibre.")


if __name__ == "__main__":
    main()
