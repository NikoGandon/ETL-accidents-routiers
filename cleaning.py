"""Nettoyage : espaces, NaN, types, decodage."""

import numpy as np
import pandas as pd

import config
from codes import DECODE_MAP


def strip_cells(df: pd.DataFrame) -> pd.DataFrame:
    """Strip toutes les cellules texte (sinon " -1" echappe aux filtres)."""
    return df.apply(lambda s: s.str.strip() if s.dtype == object else s)


def clean_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Vire les espaces dans les identifiants (separateurs de milliers).
    Sans ca les jointures cassent silencieusement.
    """
    df = df.copy()
    # \s+ couvre aussi les insecables (\xa0, \u202f)
    for col in config.ID_COLS & set(df.columns):
        df[col] = df[col].str.replace(r"\s+", "", regex=True)
    return df


def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Remplace les marqueurs vides et -1 par NaN (sauf lat/long pour -1)."""
    df = df.copy()
    df = df.replace(list(config.MISSING_TOKENS), np.nan)

    minus_one_cols = [c for c in df.columns if c not in config.MISSING_MINUS_ONE_EXCLUDE]
    df[minus_one_cols] = df[minus_one_cols].replace("-1", np.nan)
    return df


def _to_float_comma(series: pd.Series) -> pd.Series:
    """Virgule decimale -> point."""
    return pd.to_numeric(
        series.str.replace(",", ".", regex=False), errors="coerce"
    )


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes numeriques (decimales FR, entiers)."""
    df = df.copy()
    cols = set(df.columns)

    for col in config.DECIMAL_COMMA_COLS & cols:
        df[col] = _to_float_comma(df[col])

    for col in config.NUMERIC_COLS & cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # dep/com restent en str (zeros de tete, 2A/2B)
    return df


def add_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Reconstruit date_heure depuis an/mois/jour/hrmn (si les colonnes existent)."""
    if not set(config.DATE_PARTS).issubset(df.columns):
        return df
    df = df.copy()
    base = (
        df["an"].astype(str).str.zfill(4) + "-"
        + df["mois"].astype(str).str.zfill(2) + "-"
        + df["jour"].astype(str).str.zfill(2) + " "
        + df["hrmn"].fillna("00:00")
    )
    df["date_heure"] = pd.to_datetime(base, format="%Y-%m-%d %H:%M", errors="coerce")
    return df


def _normalize_code(value):
    """'07' -> '7', '2.0' -> '2', 'A' -> 'A', NaN -> NaN."""
    if pd.isna(value):
        return value
    text = str(value).strip()
    try:
        return str(int(float(text)))
    except (ValueError, TypeError):
        return text


def decode_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute <col>_lib avec le libelle en clair."""
    df = df.copy()
    for col, mapping in DECODE_MAP.items():
        if col not in df.columns:
            continue
        normalized = df[col].map(_normalize_code)
        df[f"{col}_lib"] = normalized.map(mapping)
    return df


def clean_table(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline complet de nettoyage sur un fichier."""
    df = strip_cells(df)
    df = clean_ids(df)
    df = clean_missing(df)
    df = fix_types(df)
    df = add_datetime(df)
    df = decode_labels(df)
    return df
