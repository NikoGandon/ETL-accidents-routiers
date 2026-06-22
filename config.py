"""Config du pipeline BAAC / ONISR. Tous les params sont ici."""

from pathlib import Path

# Chemins & année
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ANNEE = 2024

# Noms de fichiers (varient selon les années)
FICHIERS = {
    "caract": BASE_DIR / f"caract-{ANNEE}.csv",
    "lieux": BASE_DIR / f"lieux-{ANNEE}.csv",
    "vehicules": BASE_DIR / f"vehicules-{ANNEE}.csv",
    "usagers": BASE_DIR / f"usagers-{ANNEE}.csv",
}

# Lecture
SEP = ";"
ENCODINGS = ("utf-8", "latin-1")

# Valeurs manquantes
MISSING_TOKENS = {"", ".", "N/A", "NA", "nan", "NaN"}
# -1 = "non renseigné" dans la base, sauf pour lat/long
MISSING_MINUS_ONE_EXCLUDE = {"lat", "long"}

# Groupes de colonnes (noms en minuscules apres standardisation)
ID_COLS = {"num_acc", "id_vehicule", "id_usager"}
DECIMAL_COMMA_COLS = {"lat", "long", "lartpc", "larrout"}
NUMERIC_COLS = {"nbv", "vma", "pr", "pr1", "occutc", "an_nais"}
KEEP_AS_STRING = {"dep", "com"}  # zeros de tete, 2A/2B
DATE_PARTS = ("an", "mois", "jour", "hrmn")
