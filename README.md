superuser
Username (leave blank to use 'jacob.moore'): 
Email address: jacob.w.moore@gmail.com

Cat

How to run Python App
source venv/bin/activate

Windows: venv\Scripts\activate.

python manage.py runserver

How to run Angular
ng build
ng serve


How to run Python script
Start in virtual environment: source venv/bin/activate
Load up shell: python manage.py shell
from league.import_enrollment_data import import_enrollment_data
import_enrollment_data()


# How to delete data from Python
from league.models import Player

# Delete all Player records
Player.objects.all().delete()

/littleleague_backend    # Python/Django backend
/league                  # Django app inside backend
/littleleague_frontend   # Angular project

pip list
Package                       Version
----------------------------- -----------
asgiref                       3.8.1
branca                        0.8.1
certifi                       2025.1.31
charset-normalizer            3.4.1
Django                        4.2.20
django-cors-headers           4.7.0
djangorestframework           3.15.2
djangorestframework_simplejwt 5.5.0
folium                        0.19.5
geographiclib                 2.0
geopandas                     1.0.1
geopy                         2.4.1
idna                          3.10
Jinja2                        3.1.6
MarkupSafe                    3.0.2
numpy                         2.0.2
packaging                     24.2
pandas                        2.2.3
pip                           25.0.1
PyJWT                         2.9.0
pyogrio                       0.10.0
pyproj                        3.6.1
python-dateutil               2.9.0.post0
pytz                          2025.1
requests                      2.32.3
setuptools                    58.0.4
shapely                       2.0.7
six                           1.17.0
sqlparse                      0.5.3
typing_extensions             4.12.2
tzdata                        2025.1
urllib3                       2.3.0
watchdog                      6.0.0
xyzservices                   2025.1.0



1. CSV upload
2. CSV parse
3. Store data
4. Pass data to API for coordinates
5. Store coordinates
6. Display coordinates
7. Display KML data
8. Compare coordinates against KML

Here Maps
App Id: ie6q3d86kTue7uKZ8dXH
API Key: 3i6_xUsn7eU66y5VdaXzha5qwP_lFolNDSH9NUuPerc



1. Admin completion
2. Update models: Divisions, Team Names, Evaluation scores
3. Create evaluation score intake form on frontend
4. Populate evaluation score intake form with real data - update Google Sheet
5. Button for CSV upload - KML
6. Button for CSV upload - Enrollment Data
7. Button for Geocode
8. Button for compare

Reference for Budget tracking: https://youtu.be/g9VLt1OcFbg?si=kYrfuZhFO8FD6zst
Budget Tracking
Fundraising Tracking

Budget modules:
- Login and Register
- Dashboard
- Income
- Expense

### Notes:
Dashboard component
Expense component
Income component
Login component

Fundraising modules:
- Login
- Dashboard


