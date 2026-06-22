"""Fusion des 4 tables en une seule (grain = usager).
Dedup + left joins + check d'integrite.
"""

import pandas as pd


def _dedup(df: pd.DataFrame, keys: list[str], label: str, stats: dict) -> pd.DataFrame:
    """Dedup sur les cles, compte les doublons vires."""
    avant = len(df)
    df = df.drop_duplicates(subset=keys, keep="first")
    stats[f"doublons_retires_{label}"] = avant - len(df)
    return df


def merge_sources(tables: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    """Fusionne les 4 tables, renvoie (df, stats)."""
    stats: dict[str, int] = {}

    usagers = tables["usagers"]
    vehicules = _dedup(tables["vehicules"], ["num_acc", "id_vehicule"], "vehicules", stats)
    caract = _dedup(tables["caract"], ["num_acc"], "caract", stats)
    lieux = _dedup(tables["lieux"], ["num_acc"], "lieux", stats)

    n_usagers = len(usagers)
    stats["usagers_initial"] = n_usagers

    df = usagers.merge(
        vehicules, on=["num_acc", "id_vehicule"], how="left",
        validate="m:1", suffixes=("", "_veh"),
    )
    df = df.merge(caract, on="num_acc", how="left", validate="m:1", suffixes=("", "_car"))
    df = df.merge(lieux, on="num_acc", how="left", validate="m:1", suffixes=("", "_lieu"))

    # Colonnes dupliquees par les suffixes
    redundantes = [c for c in df.columns if c.endswith(("_veh", "_car", "_lieu"))]
    df = df.drop(columns=redundantes)

    stats["lignes_finales"] = len(df)
    stats["integrite_ok"] = bool(len(df) == n_usagers)
    if not stats["integrite_ok"]:
        raise RuntimeError(
            f"Intégrité rompue : {len(df)} lignes finales != {n_usagers} usagers. "
            "Une clé de jointure n'est pas unique du côté droit."
        )
    return df, stats
