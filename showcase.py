"""Genere les visuels avant/apres pour le portfolio.
Usage : python showcase.py (apres main.py)
"""

import json

import matplotlib.pyplot as plt
import pandas as pd

import config

# Colonnes affichees + renommage
COLONNES_VITRINE = {
    "date_heure": "Date & heure",
    "dep": "Dép.",
    "agg_lib": "Localisation",
    "atm_lib": "Météo",
    "surf_lib": "État surface",
    "catv_lib": "Véhicule",
    "catu_lib": "Usager",
    "age": "Âge",
    "sexe_lib": "Sexe",
    "grav_lib": "Gravité",
}
N_LIGNES = 14


def _charger_table_finale() -> pd.DataFrame:
    """Charge la table nettoyee (parquet ou csv)."""
    parquet = config.OUTPUT_DIR / f"accidents_{config.ANNEE}_propre.parquet"
    csv = config.OUTPUT_DIR / f"accidents_{config.ANNEE}_propre.csv"
    if parquet.exists():
        return pd.read_parquet(parquet)
    if csv.exists():
        return pd.read_csv(csv, low_memory=False)
    raise FileNotFoundError("Lance main.py d'abord.")


def _extrait_vitrine(df: pd.DataFrame) -> pd.DataFrame:
    """Sous-ensemble lisible pour le visuel."""
    df = df.copy()
    if "an_nais" in df.columns:
        df["age"] = (config.ANNEE - pd.to_numeric(df["an_nais"], errors="coerce"))
        df["age"] = df["age"].astype("Int64")
    if "date_heure" in df.columns:
        df["date_heure"] = pd.to_datetime(df["date_heure"], errors="coerce")

    extrait = df[list(COLONNES_VITRINE)].head(N_LIGNES).copy()
    extrait = extrait.rename(columns=COLONNES_VITRINE)
    # pas de NaN dans le visuel
    return extrait.fillna("Non renseigné").astype(str)


def _rendre_table(ax, df: pd.DataFrame, titre: str) -> None:
    """Affiche un df en table matplotlib."""
    ax.axis("off")
    ax.set_title(titre, fontsize=13, fontweight="bold", loc="left", pad=12)
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="upper left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.5)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    for (row, _col), cell in table.get_celld().items():
        cell.set_edgecolor("#d9dee3")
        if row == 0:
            cell.set_facecolor("#2563eb")
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f4f6f9")


def _charger_stats() -> dict:
    path = config.OUTPUT_DIR / "stats.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def vitrine_apres(extrait: pd.DataFrame) -> None:
    """Image de la table nettoyee seule."""
    fig, ax = plt.subplots(figsize=(13, 5))
    _rendre_table(ax, extrait, "Donnees accidents 2024 - nettoyees et decodees")
    fig.tight_layout()
    fig.savefig(config.OUTPUT_DIR / "vitrine_apres.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def vitrine_avant_apres(extrait: pd.DataFrame) -> None:
    """Montage avant/apres avec les metriques."""
    brut_lines = []
    with open(config.FICHIERS["caract"], encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 3:
                break
            brut_lines.append(line.rstrip("\n")[:110] + " …")
    texte_brut = "\n".join(brut_lines)

    stats = _charger_stats()
    metrique = (
        f"4 fichiers hétérogènes ({stats.get('lignes_brutes', '?'):,} lignes) "
        f"fusionnés, nettoyés et traduits en {stats.get('duree_traitement_s', '?')} s"
    ).replace(",", " ")

    fig = plt.figure(figsize=(13, 8.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.4], hspace=0.35)

    ax_avant = fig.add_subplot(gs[0])
    ax_avant.axis("off")
    ax_avant.set_title("AVANT - 4 CSV bruts : separateurs ';', codes, valeurs masquees",
                       fontsize=13, fontweight="bold", loc="left", color="#b91c1c")
    ax_avant.text(
        0.0, 0.75, texte_brut, family="monospace", fontsize=8.5,
        va="top", ha="left", transform=ax_avant.transAxes,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#fef2f2", edgecolor="#fca5a5"),
    )

    ax_apres = fig.add_subplot(gs[1])
    _rendre_table(ax_apres, extrait, "APRES - 1 table unique, decodee et lisible")

    fig.suptitle(metrique, fontsize=15, fontweight="bold", y=0.99)
    fig.savefig(config.OUTPUT_DIR / "vitrine_avant_apres.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = _charger_table_finale()
    extrait = _extrait_vitrine(df)
    vitrine_apres(extrait)
    vitrine_avant_apres(extrait)
    print("Visuels générés dans output/ :")
    print("  - vitrine_apres.png")
    print("  - vitrine_avant_apres.png")


if __name__ == "__main__":
    main()
