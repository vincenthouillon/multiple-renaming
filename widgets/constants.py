""" List of constants. """

ARGUMENTS_LIST = [
    "Pas de changement",
    "Nom du fichier en minuscules",
    "Nom du fichier en majuscules",
    "Extension en minuscules",
    "Extension en majuscules",
    "Tout en minuscules",
    "Tout en majuscules",
    "Première lettre de chaque mot en majuscules",
    "Première lettre de chaque mot en majuscules, sauf extension",
    "Première lettre en majuscule"
]

OPTIONS_LIST = {
    "Nom"                        : ("option_01", "[n]"),
    "Nom - premiers caractères x": ("option_01", "[nx]"),
    "Nom - derniers caractères x": ("option_01", "[n-x]"),
    "Nom - à partir de x"        : ("option_01", "[n,x]"),
    "Extension"                  : ("option_02", "[e] "),
    "Compteur"                   : ("option_02", "[c]"),
    "Date - actuelle"            : ("option_02", "[d]"),

}
