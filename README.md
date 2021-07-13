# Internship Gratification Calculator
**Version 1.0**

Outil de calcul du nombre d'heures de travail et de la gratification résultante

## Requis
- Python 3+

## Dépendances
- Python modules `sys`, `datetime`

## Utilisation
Télécharger le projet, et ouvrir le dossier en invite de commande
```shell
py internship_gratifications.py [date_debut] [date_fin] [nombre_jours_par_semaine] [nombre_heures_par_semaine] [gratification] *[jours_exceptionnels]*
```
`date_debut`                   : Date de début de stage. Format JJ/MM/AAAA *(ex: 13/07/2021)*

`date_fin`                     : Date de fin de stage. Format JJ/MM/AAAA *(ex: 13/07/2021)*

`nombre_jours_par_semaine`     : Nombre de jours de stage par semaine *(ex: 5)*

`nombre_heures_par_semaine`    : Nombre d'heures de stage par jour *(ex: 5)*

`gratification`                : Gratification du stage *(ex: 3.9)*

`Jours_exceptionnels`          : Facultatif. Les jours exceptionnels de travail si existants, à indiquer en anglais, et séparés par `,`. Par défaut, les jours **Samedi et Dimanche** sont exclus de la semaine de travail.

Devant le nom du jour, indiquer `-` pour un jour de non travail exceptionnel et `+` pour un jour de travail exceptionnel.

Exemple : `Ajouter \"+Saturday,-Monday\" en fin de ligne, si exceptionnellement vous travaillez le Samedi et ne travaillez pas le Lundi.`

## Exemple d'utilisation
![Exemple d'utilisation](https://github.com/fm16191/internship_gratifications/blob/master/usage.png?raw=true)

## Notes.
Au dessus de 2 mois de stage (équivalent de 44 jours de 7 heures de stage), une gratification de minimum 3.9€ à l'heure est obligatoire

Au dessus de 2 mois de stage, la possibilité de pouvoir poser des jours de congés est obligatoire, mais leur rémunération est facultative.

En savoir plus sur les articles du [service-public.fr](https://www.service-public.fr/professionnels-entreprises/vosdroits/F20559) ou [travail-emploi.gouv.fr](https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/article/les-stages-etudiants-en-milieu-professionnel)