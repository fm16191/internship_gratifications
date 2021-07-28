import sys, argparse
from datetime import datetime
from datetime import date
from datetime import timedelta

import os
import json
import requests

######################## FRENCH LOCAL AREA ########################

# local_area = "alsace-moselle"
# local_area = "guadeloupe"
# local_area = "guyane"
# local_area = "la-reunion"
# local_area = "martinique"
# local_area = "mayotte"
local_area = "metropole"
# local_area = "nouvelle-caledonie"
# local_area = "polynesie-francaise"
# local_area = "saint-barthelemy"
# local_area = "saint-martin"
# local_area = "saint-pierre-et-miquelon"
# local_area = "wallis-et-futuna"

# Local area is needed for public holidays dates

######################## END FOR FRENCH LOCAL AREA ########################

# Input Verification
parser = argparse.ArgumentParser(description="Outil de calcul du nombre d'heures de travail et de la gratification résultante")
parser.add_argument("date_debut", type=lambda s: datetime.strptime(s, '%d/%m/%Y'), help="date de début de stage (JJ/MM/AAAA)")
parser.add_argument("date_fin", type=lambda s: datetime.strptime(s, '%d/%m/%Y'), help="date de fin de stage (JJ/MM/AAAA)")

parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
parser.add_argument("-days", type=int, default=5, help="nombre de jours de stage par semaine (%(default)s par défaut)")
parser.add_argument("-hours", type=float, default=7, help="nombre d'heures de stage par jour (%(default)s par défaut)")
parser.add_argument("-grat", type=float, default=3.9, help="gratification horaire du stage (%(default)s par défaut)")
parser.add_argument("-ex", nargs='+', help="jours exceptionnels de travail si existants")


args = parser.parse_args()
if args.date_debut < args.date_fin:
    date_begin = args.date_debut
    date_end = args.date_fin
else:
    date_end = args.date_debut
    date_begin = args.date_fin

try:
    days_per_week = args.days
    if days_per_week < 0 or days_per_week > 7:
        raise Exception("NotPositive")
except Exception as e:
    print("Le nombre de jours de stage par semaine doit être un entier positif et inférieur à 8")
    sys.exit(1)

try:
    hours_per_day = args.hours
    if hours_per_day < 0:
        raise Exception("NotPositive")
except Exception as e:
    print("Le nombre d'heures de stage par jour doit être un entier positif")
    sys.exit(1)

try:
    gratification = args.grat
    if gratification < 0:
        raise Exception("NotPositive")
except Exception as e:
    print("La gratification doit être indiquée comme un flottant positif")
    sys.exit(1)


# Get local public holidays during years of the internship

def get_local_public_holidays(local_area, year):
    """ Store it into a file local public holidays for a year in an area if it doesn't already exist (request on api.gouv.fr) """
    filename = f"{local_area}_{year}.json"

    if not os.path.exists(filename):
        print(f"Loading public holidays for {local_area}_{year}")

        link = f"https://calendrier.api.gouv.fr/jours-feries/{filename.replace('_','/')}"
        try:
            res = requests.get(link, allow_redirects=True)
            if not res.status_code == 200:
                raise Exception(res.status_code)
            fw = open(filename, "wb")
            fw.write(res.content)
            fw.close()
        except Exception as e:
            print("Les jours fériés ne peuvent pas être téléchargés.\nLes dates données ici peuvent être supérieures à la réalité")


start_int_year = date_begin.year
end_int_year = date_end.year
public_holidays_local = {}
while start_int_year <= end_int_year:
    filename = f"{local_area}_{start_int_year}.json"
    get_local_public_holidays(local_area, start_int_year)

    if os.path.exists(filename):
        fo = open(filename, "r")
        public_holidays_local.update(json.loads("".join(fo.readlines())))
        fo.close()

    start_int_year += 1

# Gratification calculation

not_working_days = ["saturday", "sunday"]
if days_per_week < 5:
    try:
        days_str = sys.argv[6].split(",")
        for day in days_str:
            if day.startswith("-"):
                not_working_days.append(day[1:])
            elif day.startswith("+") and day[1:].lower() in not_working_days:
                del not_working_days[day[1:]]
    except Exception as e:
        print("Moins de 5j de stage par semaine, mais aucun jour de non travail spécifié.\n > Ajouter \"+Saturday,-Monday\" en fin de ligne de commande pour préciser que vous travailler les Samedis, mais pas les Lundis.")

# gratification = 3.9

all_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

working_days_name = []
for day in all_days:
    if not day in not_working_days:
        working_days_name.append(day)

working_days = 0
completed_days = 0
hours = 0
free_days_off = 0
free_days_off_dict = []

for i in range((date_end - date_begin).days + 1):
    day = date(date_begin.year, date_begin.month, date_begin.day) + timedelta(days=i)
    day_name = day.strftime("%A")
    day_strftime = day.strftime("%Y-%m-%d")
    # print(day_name)
    if not day_name.lower() in not_working_days :
        if day_strftime in public_holidays_local:
            free_days_off_dict.append(f"{public_holidays_local[day_strftime]} {day_strftime[:4]}")
            free_days_off += 1
            continue
        hours += hours_per_day
        working_days += 1
        if day < date.today():
            completed_days += 1
        # print(hours)

working_hours_count = working_days*hours_per_day
completed_hours_count = completed_days*hours_per_day
gratification_count = working_days*hours_per_day*gratification

days_off = 0 if working_hours_count <=44*7 else working_hours_count/(22*7)*2.5

# Output

print(f"\n==== Du {date_begin.strftime('%m/%d/%Y')} Au {date_end.strftime('%m/%d/%Y')}")
print(f"==== {hours_per_day} heures par jour | {gratification}€ par heure")
print(f"==== Jours de stage  : {','.join(working_days_name)}\n")
print(f"> Nombre total de jours de stage           : {working_days}")
print(f"> Nombre total d'heures de stage           : {working_hours_count}")
print(f"> Jours feriés pendant votre stage         : {free_days_off} (Relancez avec -v pour voir le détail)")
if args.verbose:
    for day_off in free_days_off_dict:
        print('\t\033[30;1m' + day_off + '\033[0m')

print(f"> Estimation gratification totale          : {gratification_count:.1f}")
print(f"> Estimation du nombre de jours de congé   : {days_off:.1f}")

print(f"\n> Progression jours de stage               : {completed_days/working_days*100:.1f}% ({completed_days}/{working_days} | {working_days-completed_days} restants)")
print(f"> Progression heures de stage              : {completed_hours_count/working_hours_count*100:.1f}% ({completed_hours_count}/{working_hours_count} | {working_hours_count-completed_hours_count} restantes)")
print("\nDisclaimer: La gratification et les jours de congés sont des estimations, et peuvent différer en fonction de l'employeur.")