""" List of constants. """

ARGUMENTS_DICT = {
    0: "Pas de changement",
    1: "Nom du fichier en minuscules",
    2: "Nom du fichier en majuscules",
    3: "Extension en minuscules",
    4: "Extension en majuscules",
    5: "Tout en minuscules",
    6: "Tout en majuscules",
    7: "Première lettre de chaque mot en majuscules",
    8: "Première lettre en majuscule"
}

OPTIONS_DICT = {
    "[n]"  : "Nom [n]",
    "[nx]" : "Nom - premiers caractères x [nx]",
    "[n-x]": "Nom - derniers caractères x [n-x]",
    "[n,x]": "Nom - à partir de x [n,x]",
    "[c]"  : "Compteur [c]",
    "[d]"  : "Date - actuelle [d]"
}

DATE_FORMAT_LIST = [
    "yyyy-mm-dd hh-nn-ss",
    "yyyymmdd",
]

"""
Option(s) supprimée(s):

    "[e]"  : "Extension [e]",
"""
