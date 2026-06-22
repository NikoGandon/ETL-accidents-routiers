"""Chargement brut des CSV BAAC (tout en str, on type apres)."""

from pathlib import Path

import pandas as pd

import config


def load_raw(path: Path) -> pd.DataFrame:
    """Lit un CSV en str avec auto-detection de l'encodage."""
    last_error = None
    for enc in config.ENCODINGS:
        try:
            return pd.read_csv(
                path,
                sep=config.SEP,
                dtype=str,
                encoding=enc,
                keep_default_na=False,
            )
        except (UnicodeDecodeError, UnicodeError) as exc:
            last_error = exc
    raise UnicodeError(f"Aucun encodage n'a fonctionné pour {path} : {last_error}")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Noms de colonnes en minuscules, sans espaces."""
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def load_all() -> dict[str, pd.DataFrame]:
    """Charge les 4 fichiers, renvoie {nom: df}."""
    tables = {}
    for nom, path in config.FICHIERS.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Fichier introuvable : {path}\n"
                f"Vérifie l'année ({config.ANNEE}) et les noms dans config.FICHIERS."
            )
        tables[nom] = standardize_columns(load_raw(path))
    return tables
