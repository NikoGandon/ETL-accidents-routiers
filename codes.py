"""Dictionnaires de decodage (source : doc ONISR).
Cles = codes en str, valeurs = libelles. Colonne creee : <col>_lib.
"""

# --- CARACTERISTIQUES ------------------------------------------------------ #
LUM = {
    "1": "Plein jour",
    "2": "Crépuscule ou aube",
    "3": "Nuit sans éclairage public",
    "4": "Nuit avec éclairage public non allumé",
    "5": "Nuit avec éclairage public allumé",
}
AGG = {"1": "Hors agglomération", "2": "En agglomération"}
INT = {
    "1": "Hors intersection", "2": "Intersection en X", "3": "Intersection en T",
    "4": "Intersection en Y", "5": "Intersection à plus de 4 branches",
    "6": "Giratoire", "7": "Place", "8": "Passage à niveau", "9": "Autre intersection",
}
ATM = {
    "1": "Normale", "2": "Pluie légère", "3": "Pluie forte", "4": "Neige - grêle",
    "5": "Brouillard - fumée", "6": "Vent fort - tempête", "7": "Temps éblouissant",
    "8": "Temps couvert", "9": "Autre",
}
COL = {
    "1": "2 véh. - frontale", "2": "2 véh. - par l'arrière", "3": "2 véh. - par le côté",
    "4": "3 véh.+ - en chaîne", "5": "3 véh.+ - collisions multiples",
    "6": "Autre collision", "7": "Sans collision",
}

# --- LIEUX ----------------------------------------------------------------- #
CATR = {
    "1": "Autoroute", "2": "Route nationale", "3": "Route départementale",
    "4": "Voie communale", "5": "Hors réseau public",
    "6": "Parc de stationnement", "7": "Route de métropole urbaine", "9": "Autre",
}
CIRC = {
    "1": "Sens unique", "2": "Bidirectionnelle", "3": "Chaussées séparées",
    "4": "Voies d'affectation variable",
}
VOSP = {
    "0": "Sans objet", "1": "Piste cyclable", "2": "Bande cyclable", "3": "Voie réservée",
}
PROF = {"1": "Plat", "2": "Pente", "3": "Sommet de côte", "4": "Bas de côte"}
PLAN = {
    "1": "Rectiligne", "2": "Courbe à gauche", "3": "Courbe à droite", "4": "En S",
}
SURF = {
    "1": "Normale", "2": "Mouillée", "3": "Flaques", "4": "Inondée", "5": "Enneigée",
    "6": "Boue", "7": "Verglacée", "8": "Corps gras - huile", "9": "Autre",
}
INFRA = {
    "0": "Aucun", "1": "Souterrain - tunnel", "2": "Pont - autopont",
    "3": "Bretelle d'échangeur", "4": "Voie ferrée", "5": "Carrefour aménagé",
    "6": "Zone piétonne", "7": "Zone de péage", "8": "Chantier", "9": "Autres",
}
SITU = {
    "0": "Aucun", "1": "Sur chaussée", "2": "Sur bande d'arrêt d'urgence",
    "3": "Sur accotement", "4": "Sur trottoir", "5": "Sur piste cyclable",
    "6": "Sur autre voie spéciale", "8": "Autres",
}

# --- VEHICULES ------------------------------------------------------------- #
SENC = {
    "0": "Inconnu", "1": "PR croissant", "2": "PR décroissant", "3": "Absence de repère",
}
CATV = {
    "0": "Indéterminable", "1": "Bicyclette", "2": "Cyclomoteur <50cm3",
    "3": "Voiturette", "7": "VL seul", "10": "VU 1,5-3,5T", "13": "PL 3,5-7,5T",
    "14": "PL >7,5T", "15": "PL >3,5T + remorque", "16": "Tracteur routier seul",
    "17": "Tracteur routier + semi", "20": "Engin spécial", "21": "Tracteur agricole",
    "30": "Scooter <50cm3", "31": "Moto 50-125cm3", "32": "Scooter 50-125cm3",
    "33": "Moto >125cm3", "34": "Scooter >125cm3", "35": "Quad léger <=50cm3",
    "36": "Quad lourd >50cm3", "37": "Autobus", "38": "Autocar", "39": "Train",
    "40": "Tramway", "41": "3RM <=50cm3", "42": "3RM 50-125cm3", "43": "3RM >125cm3",
    "50": "EDP à moteur", "60": "EDP sans moteur", "80": "VAE", "99": "Autre véhicule",
}
OBS = {
    "0": "Sans objet", "1": "Véhicule en stationnement", "2": "Arbre",
    "3": "Glissière métallique", "4": "Glissière béton", "5": "Autre glissière",
    "6": "Bâtiment, mur, pile de pont", "7": "Support signalisation/PAU", "8": "Poteau",
    "9": "Mobilier urbain", "10": "Parapet", "11": "Îlot, refuge, borne",
    "12": "Bordure de trottoir", "13": "Fossé, talus, paroi", "14": "Obstacle chaussée",
    "15": "Obstacle trottoir/accotement", "16": "Sortie de chaussée sans obstacle",
    "17": "Buse - tête d'aqueduc",
}
OBSM = {
    "0": "Aucun", "1": "Piéton", "2": "Véhicule", "4": "Véhicule sur rail",
    "5": "Animal domestique", "6": "Animal sauvage", "9": "Autre",
}
CHOC = {
    "0": "Aucun", "1": "Avant", "2": "Avant droit", "3": "Avant gauche", "4": "Arrière",
    "5": "Arrière droit", "6": "Arrière gauche", "7": "Côté droit", "8": "Côté gauche",
    "9": "Chocs multiples (tonneaux)",
}
MANV = {
    "0": "Inconnue", "1": "Sans changement de direction", "2": "Même sens, même file",
    "3": "Entre 2 files", "4": "Marche arrière", "5": "À contresens",
    "6": "Franchissant le TPC", "7": "Couloir bus même sens", "8": "Couloir bus sens inverse",
    "9": "En s'insérant", "10": "Demi-tour sur chaussée", "11": "Changeant de file à gauche",
    "12": "Changeant de file à droite", "13": "Déporté à gauche", "14": "Déporté à droite",
    "15": "Tournant à gauche", "16": "Tournant à droite", "17": "Dépassant à gauche",
    "18": "Dépassant à droite", "19": "Traversant la chaussée", "20": "Stationnement",
    "21": "Évitement", "22": "Ouverture de porte", "23": "Arrêté (hors stationnement)",
    "24": "En stationnement", "25": "Circulant sur trottoir", "26": "Autres manœuvres",
}
MOTOR = {
    "0": "Inconnue", "1": "Hydrocarbures", "2": "Hybride électrique", "3": "Électrique",
    "4": "Hydrogène", "5": "Humaine", "6": "Autre",
}

# --- USAGERS --------------------------------------------------------------- #
CATU = {"1": "Conducteur", "2": "Passager", "3": "Piéton"}
GRAV = {"1": "Indemne", "2": "Tué", "3": "Blessé hospitalisé", "4": "Blessé léger"}
SEXE = {"1": "Masculin", "2": "Féminin"}
TRAJET = {
    "0": "Non renseigné", "1": "Domicile - travail", "2": "Domicile - école",
    "3": "Courses - achats", "4": "Utilisation professionnelle",
    "5": "Promenade - loisirs", "9": "Autre",
}
SECU = {
    "0": "Aucun équipement", "1": "Ceinture", "2": "Casque", "3": "Dispositif enfants",
    "4": "Gilet réfléchissant", "5": "Airbag (2RM/3RM)", "6": "Gants (2RM/3RM)",
    "7": "Gants + Airbag", "8": "Non déterminable", "9": "Autre",
}
LOCP = {
    "0": "Sans objet", "1": "+50 m du passage piéton", "2": "-50 m du passage piéton",
    "3": "Passage piéton sans signal", "4": "Passage piéton avec signal",
    "5": "Sur trottoir", "6": "Sur accotement", "7": "Sur refuge ou BAU",
    "8": "Sur contre-allée", "9": "Inconnue",
}
ACTP = {  # A et B sont des codes alphanumeriques
    "0": "Sans objet", "1": "Sens véhicule heurtant", "2": "Sens inverse",
    "3": "Traversant", "4": "Masqué", "5": "Jouant - courant", "6": "Avec animal",
    "9": "Autre", "A": "Monte/descend du véhicule", "B": "Inconnue",
}
ETATP = {"1": "Seul", "2": "Accompagné", "3": "En groupe"}

# colonne -> dict de decodage
DECODE_MAP = {
    "lum": LUM, "agg": AGG, "int": INT, "atm": ATM, "col": COL,
    "catr": CATR, "circ": CIRC, "vosp": VOSP, "prof": PROF, "plan": PLAN,
    "surf": SURF, "infra": INFRA, "situ": SITU,
    "senc": SENC, "catv": CATV, "obs": OBS, "obsm": OBSM, "choc": CHOC,
    "manv": MANV, "motor": MOTOR,
    "catu": CATU, "grav": GRAV, "sexe": SEXE, "trajet": TRAJET,
    "secu1": SECU, "secu2": SECU, "secu3": SECU,
    "locp": LOCP, "actp": ACTP, "etatp": ETATP,
}
