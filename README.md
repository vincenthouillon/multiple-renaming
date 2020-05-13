# multiple_renaming

*Multiple Renaming application in priority for MacOS.*


## Todo:
- Ajouter support multilangues [FR/EN]
- Créer une page GitHubIo
- Menu :
    - Paramètres
    - A propos
    - Aide
- Mémorisation des paramètres
- Enregistrement de profil de renommage


```python
self.prohibited_filename = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2",
                            "COM3", "COM4", "COM5", "COM6", "COM7", "COM8",
                            "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
                            "LPT6", "LPT7", "LPT8", "LPT9"]
```


```json
{
    "French": {
        "treeview": {
            "hold_name"    : "Ancien nom de fichier",
            "new_name"     : "Nouveau nom de fichier",
            "size"         : "Taille",
            "date_modified": "Modifie le",
            "date_creation": "Créé le",
            "location"     : "Emplacement",
        },
        "arguments": {
            "0": "Pas de changement",
            "1": "Nom du fichier en minuscules",
            "2": "Nom du fichier en majuscules",
            "3": "Extension en minuscules",
            "4": "Extension en majuscules",
            "5": "Tout en minuscules",
            "6": "Tout en majuscules",
            "7": "Première lettre de chaque mot en majuscules",
            "8": "Première lettre en majuscule"
        },
        "options": {
            "[n]"  : "Nom [n]",
            "[nx]" : "Nom - premiers caractères x [nx]",
            "[n-x]": "Nom - derniers caractères x [n-x]",
            "[n,x]": "Nom - à partir de x [n,x]",
            "[c]"  : "Compteur [c]",
            "[d]"  : "Date - actuelle [d]"
        },
        "menu": {
            "open"   : "Ouvrir",
            "exit"   : "Quitter",
            "file"   : "Fichier",
            "licence": "Afficher la licence",
            "about"  : "A propos",
            "help"   : "Aide"
        },
        "statusbar": {
            "nb_files": "0 fichier(s)",
            "alert"   : "Un nom de fichier ne peut pas contenir les caractères suivants : \ / : * ? \" < > |"
        },
        "parameters": {
            "frame_method" : "Méthode",
            "lbl_filename" : "Nom de fichier   : ",
            "lbl_arguments": "Arguments        : ",
            "frame_search" : "Chercher et remplacer",
            "lbl_search"   : "Recherche        : ",
            "lbl_replace"  : "Remplacer        : ",
            "frame_counter": "Compteur",
            "lbl_start"    : "Démarrer à       : ",
            "lbl_step"     : "Pas              : ",
            "lbl_len"      : "Nombre de chiffre: ",
            "frame_date"   : "Format date/heure",
            "btn_rename"   : "✔️ Renommer",
            "check_button" : "Fermer aprés renommage."
        }
    }
}
```

module : configparser

```ini
# configuration.ini or configuration.cfg
[language]
language=French

[version]
version= 1.0
```


Modify config.cfg

```python
config["language"]["language"] = "fr"

with open("common/config.cfg", "w") as configfile:
    config.write(configfile)
```