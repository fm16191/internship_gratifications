# Internship Gratification Calculator

**Version 1.0**

Outil de calcul du nombre d'heures de travail et de la gratification résultante.

## Prérequis et dépendances

- Python 3+
- Modules Python `sys`, `datetime`, `argparse`, `json`, `requests`

## Utilisation

Télécharger le projet, et ouvrir le dossier en invite de commande

```shell
py internship_gratifications.py date_debut date_fin [-h] [-v] [-hours X] [-grat X.X] 
                                                    [-add weekday ...] [-rm weekday ...]
```

### Arguments requis

- `date_debut`  : Date de début de stage au format `JJ/MM/AAAA` *(ex: 13/07/2021)*.
- `date_fin`    : Date de fin de stage au format `JJ/MM/AAAA` *(ex: 13/07/2021)*.

### Arguments optionnels

- `-h`               : Affiche l'aide à l'utilisation
- `-v`               : Exécution en mode verbeux
- `-hours X`         : Nombre d'heures de stage par jour *(7h/j par défaut)*
- `-grat X.X`        : Gratification horaire du stage *(3.9€/h par défaut)*
- `-add weekday ...` : ajouter des jours exceptionnels de travail (saturday, sunday)
- `-rm weekday ...`  : retirer des jours de travail en semaine (monday, tuesday, ...)

> Par défaut, la semaine est définie sur 5 jours **du Lundi au Vendredi**. Utilisez les options `-add` et `-rm` pour adapter le programme à votre semaine.

### Exemple de syntaxe

- `py internship_gratifications.py 01/05/2021 06/07/2021` — Calcul du nombre d'heures de travail pour la période indiquée
- `py internship_gratifications.py 01/05/2021 06/07/2021 -hours 8 -grat 4.5` — Nombre d'heures fixées à 8h/j, gratification fixée à 4.5€/h  
- `py internship_gratifications.py 01/05/2021 06/07/2021 -add saturday -rm monday tuesday` — Semaine de travail exceptionnelle : du **Mercredi au Samedi**

## Exemple d'utilisation

![Exemple d'utilisation](https://github.com/fm16191/internship_gratifications/blob/master/usage.png?raw=true)

## Notes

Au dessus de 2 mois de stage (équivalent de 44 jours de 7 heures de stage), une gratification de **3.9€ à l'heure au minimum** est obligatoire.

Au dessus de 2 mois de stage, la possibilité de poser des jours de congés est obligatoire, mais leur rémunération est facultative.

En savoir plus sur les articles du [service-public.fr](https://www.service-public.fr/professionnels-entreprises/vosdroits/F20559) ou [travail-emploi.gouv.fr](https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/article/les-stages-etudiants-en-milieu-professionnel).
