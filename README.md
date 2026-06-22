# ETL accidents routiers (BAAC / ONISR)

Pipeline Python pour nettoyer et fusionner les 4 fichiers BAAC (caract, lieux, vehicules, usagers) en une seule table au grain usager.

Donnees : [accidents corporels sur data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

## Ce que fait le script

- lecture robuste (encodage, tout en str au depart)
- nettoyage des IDs, valeurs manquantes (-1, N/A, etc.), types
- decodage des variables codees (lum, grav, catv...)
- fusion des 4 tables avec controle d'integrite
- rapport qualite + export CSV (et Parquet si pyarrow est installe)

## Installation

```bash
pip install -r requirements.txt
```

## Donnees d'entree

Place les 4 CSV de l'anneee voulue a la racine du projet :

```
caract-2024.csv
lieux-2024.csv
vehicules-2024.csv
usagers-2024.csv
```

L'annee est configurable dans `config.py` (`ANNEE = 2024`).

## Lancement

```bash
python main.py
```

Sorties dans `output/` :

- `accidents_2024_propre.csv`
- `rapport_qualite.txt`
- `manquants_par_colonne.csv`
- `stats.json`

Visuel portfolio (HTML) :

```bash
python showcase.py
```

Genere `output/vitrine_avant_apres.html`.

## Resultats (2024)

| | |
|---|---|
| Entree | 342 515 lignes sur 4 fichiers |
| Sortie | 125 187 usagers, 85 colonnes |
| Traitement | ~12 s |

## Structure

```
config.py      # chemins, annee, colonnes
codes.py       # dictionnaires de decodage ONISR
loader.py      # chargement CSV
cleaning.py    # nettoyage et types
merging.py     # fusion
reporting.py   # rapport qualite
main.py        # orchestration
showcase.py    # visuel HTML avant/apres
```
