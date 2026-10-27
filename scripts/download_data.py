"""Télécharger les huit fichiers après charge, depuis Borealis V2.0."""
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
# Identifiants vérifiés dans la version 2.0 du jeu doi:10.80240/FK2/WRCLHO.
FILES = {
    "apr": 74320, "ar": 74314, "au": 74324, "bse": 74313,
    "lg": 74325, "li": 74312, "oem": 74326, "sg": 74329,
}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for label, file_id in FILES.items():
        target = RAW / f"ocv_relaxation_24h__24h_charge_{label}.tab"
        # L'API renvoie le format tabulé de Borealis, d'où l'extension .tab.
        with urlopen(f"https://demo.borealisdata.ca/api/access/datafile/{file_id}",
                     timeout=60) as response:
            content = response.read()
        if not content.startswith(b"Timestamp [h]\t"):
            raise ValueError(f"Réponse inattendue pour {target.name}")
        temporary = target.with_suffix(".tmp")
        temporary.write_bytes(content)
        temporary.replace(target)
        print(f"Téléchargé : {target.name}", flush=True)


if __name__ == "__main__":
    main()
