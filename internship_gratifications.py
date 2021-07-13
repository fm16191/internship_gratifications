import sys
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

if not len(sys.argv) >= 6:
    print("Command format is incorrect.")
    print("Example command : py internship_gratifications.py 13/07/2021 20/10/2021 5 7 3.9")
    exit()

try:
    date_begin_str = sys.argv[1]
    # date_begin_str = "28/09/2020"
    date_begin = datetime.strptime(date_begin_str, '%d/%m/%Y')
except Exception as e:
    print("Date format is incorrect, use DD/MM/YYYY")
    exit()

try:
    date_end_str = sys.argv[2]
    # date_end_str = "15/01/2021"
    date_end = datetime.strptime(date_end_str, '%d/%m/%Y')
except Exception as e:
    print("Date format is incorrect, use DD/MM/YYYY")
    exit()

if date_begin > date_end:
    print("End date must be after begin date")
    exit()

try:
    # days_per_week = 35
    days_per_week = int(sys.argv[3])
    if days_per_week < 0:
        raise Exception("NotPositive")
except Exception as e:
    print("Days per week should be a positive integer")
    exit()

try:
    # hours_per_day = 7
    hours_per_day = int(sys.argv[4])
    if hours_per_day < 0:
        raise Exception("NotPositive")
except Exception as e:
    print("Hours per day should be a positive integer")
    exit()

try:
    gratification = float(sys.argv[5])
    if gratification < 0:
        raise Exception("NotPositive")
except Exception as e:
    print("Gratification should be a positive float")
    exit()


# Get local public holidays

filename = f"{local_area}_{datetime.today().year}.json"

if not os.path.exists(filename):
    print(f"Loading public holidays for {local_area}_{datetime.today().year}")

    link = f"https://calendrier.api.gouv.fr/jours-feries/{filename.replace('_','/')}"
    try:
        res = requests.get(link, allow_redirects=True)
        if not res.status_code == 200:
            raise Exception(res.status_code)
        fw = open(filename, "wb")
        fw.write(res.content)
        fw.close()
    except Exception as e:
        print("Public holidays couldn't be downloaded for some reason.")
        print("Dates may therefore be wrong")

public_holidays_local = {}
if os.path.exists(filename):
    fo = open(filename, "r")
    public_holidays_local = json.loads("".join(fo.readlines()))
    fo.close()


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
        print("Days per week < 5 but not working days not specified or wrong format. Add \"+Saturday,-Monday\" at end line for example if you work on Saturdays and not on Mondays ")

# gratification = 3.9

all_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

working_days_name = []
for day in all_days:
    if not day in not_working_days:
        working_days_name.append(day)

working_days = 0
completed_days = 0
hours = 0

for i in range((date_end - date_begin).days + 1):
    day = date(date_begin.year, date_begin.month, date_begin.day) + timedelta(days=i)
    day_name = day.strftime("%A")
    day_strftime = day.strftime("%Y-%m-%d")
    if day_strftime in public_holidays_local:
        continue
    # print(day_name)
    if not day_name.lower() in not_working_days :
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

print(f"\n==== FROM {date_begin_str} TO {date_end_str}")
print(f"==== {hours_per_day} hours a day | {gratification}€ per hour")
print(f"==== Working days  : {','.join(working_days_name)}\n")
print(f"> Working days count            : {working_days}")
print(f"> Working hours count           : {working_hours_count}")
print(f"> Estimated gratification total : {gratification_count:.1f}")
print(f"> Estimated days off count      : {days_off:.1f}")

print(f"\n> Completed days so far         : {completed_days/working_days*100:.1f}% ({completed_days}/{working_days} | {working_days-completed_days} left)")
print(f"> Completed hours so far        : {completed_hours_count/working_hours_count*100:.1f}% ({completed_hours_count}/{working_hours_count} | {working_hours_count-completed_hours_count} left)")
print("\nDisclaimer: Gratification and days off counts are estimations, and might differs depending on your employer")