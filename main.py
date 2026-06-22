"""Pipeline BAAC/ONISR : charge, nettoie, fusionne et exporte.
Usage : python main.py
"""

import json
import time

import config
import loader
import cleaning
import merging
import reporting


def export(df, basename: str) -> None:
    """CSV + Parquet (si pyarrow dispo)."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = config.OUTPUT_DIR / f"{basename}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  CSV     -> {csv_path}")

    try:
        parquet_path = config.OUTPUT_DIR / f"{basename}.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"  Parquet -> {parquet_path}")
    except (ImportError, ValueError):
        print("  Parquet -> skip (pyarrow pas installe)")


def main() -> None:
    print(f"\n[1/4] Chargement des fichiers {config.ANNEE}...")
    raw_tables = loader.load_all()
    # copie brute pour le rapport avant/apres
    raw_for_report = {k: v.copy() for k, v in raw_tables.items()}
    lignes_brutes = sum(len(df) for df in raw_tables.values())

    # chrono du traitement (hors I/O)
    t0 = time.perf_counter()

    print("[2/4] Nettoyage de chaque rubrique...")
    clean_tables = {nom: cleaning.clean_table(df) for nom, df in raw_tables.items()}

    print("[3/4] Fusion des 4 rubriques (grain : usager)...")
    final_df, merge_stats = merging.merge_sources(clean_tables)

    duree = time.perf_counter() - t0

    print("[4/4] Rapport qualité + export...")
    rapport = reporting.build_report(raw_for_report, final_df, merge_stats)
    export(final_df, f"accidents_{config.ANNEE}_propre")

    # stats pour showcase.py
    stats = {
        "annee": config.ANNEE,
        "lignes_brutes": lignes_brutes,
        "lignes_finales": merge_stats["lignes_finales"],
        "colonnes_finales": int(final_df.shape[1]),
        "duree_traitement_s": round(duree, 2),
    }
    (config.OUTPUT_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n" + rapport)
    print(f"\n  Traitement (nettoyage + fusion) : {duree:.2f} s\n")


if __name__ == "__main__":
    main()
