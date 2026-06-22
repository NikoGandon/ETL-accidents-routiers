"""Rapport qualite avant/apres + detail des NaN par colonne."""

import pandas as pd

import config


def _count_raw_missing(df: pd.DataFrame) -> int:
    """Compte les cellules vides ou -1 dans la table brute."""
    stripped = df.apply(lambda s: s.str.strip())
    masque = stripped.isin(config.MISSING_TOKENS) | (stripped == "-1")
    return int(masque.to_numpy().sum())


def summarize_raw(raw_tables: dict[str, pd.DataFrame]) -> dict:
    """Stats d'entree par fichier."""
    resume = {}
    for nom, df in raw_tables.items():
        cells = df.size
        manquants = _count_raw_missing(df)
        resume[nom] = {
            "lignes": len(df),
            "colonnes": df.shape[1],
            "manquants_masques": manquants,
            "pct_manquants": round(100 * manquants / cells, 2) if cells else 0.0,
        }
    return resume


def missing_per_column(final_df: pd.DataFrame) -> pd.DataFrame:
    """NaN par colonne dans la table finale."""
    n = len(final_df)
    miss = final_df.isna().sum().sort_values(ascending=False)
    return pd.DataFrame(
        {
            "colonne": miss.index,
            "nb_manquants": miss.values,
            "pct_manquants": (100 * miss.values / n).round(2),
        }
    )


def build_report(
    raw_tables: dict[str, pd.DataFrame],
    final_df: pd.DataFrame,
    merge_stats: dict,
) -> str:
    """Genere et ecrit le rapport qualite."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = summarize_raw(raw_tables)
    miss_col = missing_per_column(final_df)
    miss_col.to_csv(config.OUTPUT_DIR / "manquants_par_colonne.csv", index=False)

    lignes_brutes = sum(v["lignes"] for v in raw.values())
    lib_cols = [c for c in final_df.columns if c.endswith("_lib")]

    L = []
    L.append("=" * 64)
    L.append(f"  RAPPORT QUALITÉ — Accidents corporels {config.ANNEE} (BAAC/ONISR)")
    L.append("=" * 64)
    L.append("")
    L.append("ENTRÉE (données brutes)")
    L.append("-" * 64)
    for nom, s in raw.items():
        L.append(
            f"  {nom:<12} {s['lignes']:>8} lignes | {s['colonnes']:>2} col. | "
            f"manquants masqués : {s['pct_manquants']:>5} %"
        )
    L.append(f"  {'TOTAL':<12} {lignes_brutes:>8} lignes réparties sur 4 fichiers")
    L.append("")
    L.append("OPÉRATIONS DE NETTOYAGE")
    L.append("-" * 64)
    L.append("  - séparateur ';' + guillemets gérés")
    L.append("  - décimales françaises (lat/long, largeurs) converties en float")
    L.append("  - identifiants : espaces de milliers supprimés (jointures fiables)")
    L.append("  - 3 formes de manquants ('-1', '', 'N/A') -> vrais NaN")
    L.append(f"  - {len(lib_cols)} variables codées décodées en libellés lisibles")
    for k, v in merge_stats.items():
        if k.startswith("doublons_retires"):
            L.append(f"  - {k.replace('_', ' ')} : {v}")
    L.append("")
    L.append("SORTIE (table consolidée)")
    L.append("-" * 64)
    L.append(f"  grain                : 1 ligne / usager")
    L.append(f"  lignes               : {merge_stats['lignes_finales']}")
    L.append(f"  colonnes             : {final_df.shape[1]}")
    L.append(f"  intégrité jointure   : {'OK' if merge_stats['integrite_ok'] else 'ÉCHEC'}")
    L.append("")
    L.append("  Top colonnes les plus incomplètes (après nettoyage) :")
    for _, r in miss_col.head(8).iterrows():
        L.append(f"    {r['colonne']:<18} {r['pct_manquants']:>6} % manquants")
    L.append("")
    L.append("=" * 64)
    L.append("  4 fichiers bruts hétérogènes  ->  1 table propre, typée, lisible")
    L.append("=" * 64)

    rapport = "\n".join(L)
    (config.OUTPUT_DIR / "rapport_qualite.txt").write_text(rapport, encoding="utf-8")
    return rapport
