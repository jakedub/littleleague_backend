import os
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ValidationError
from league.models import Player
from league.views import check_player_in_district, parse_kml

class Command(BaseCommand):
    help = 'Updates players with district information'
    
    def import_enrollment_data(self):
        from ...models import Player, Team 
        csv_file_path = os.path.join('static', 'Enrollment Address.csv')
        if not os.path.exists(csv_file_path):
            print(f"File not found: {csv_file_path}")
            return False
        df = pd.read_csv(csv_file_path)
        geolocator = Nominatim(user_agent="myApp")
        failed_geocoding = []

        max_retries = 3
        retry_delay = 2 

        for index, row in df.iterrows():
            street_address = row['Street Address']
            city = row['City']
            state = row['State']
            postal_code = row['Postal Code']

            address = f"{street_address}, {city}, {state}, {postal_code}"

            print(f"Attempting to geocode: {address}")

            location = None
            retries = 0
            while retries < max_retries and location is None:
                try:
                    location = geolocator.geocode(address, timeout=10) 
                    if location:
                        print(f"Geocoding successful for: {address}")
                        break  
                    else:
                        print(f"Geocoding returned None for {address}")
                        break
                except (GeocoderTimedOut, GeocoderUnavailable) as e:
                    retries += 1
                    print(f"Geocoding failed for {address}. Retrying {retries}/{max_retries}...")
                    sleep(retry_delay) 
                except Exception as e:
                    print(f"Unexpected error occurred for {address}: {e}")
                    break  

            if location:
                team_name = row['Division Name'] 
                team, created = Team.objects.get_or_create(name=team_name, city=row['City'])  
                player = Player(
                    first_name=row['Player First Name'],
                    last_name=row['Player Last Name'],
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    team=team,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    district=True  # Explicitly set district to True when geocoding is successful
                )
                player.save()
                print(f"Player {player.first_name} {player.last_name} saved.")
            else:
                # If geocoding failed, set latitude and longitude to None
                team_name = row['Division Name']  # Assuming team information exists in the CSV
                team, created = Team.objects.get_or_create(name=row['Division Name'], city=row['City'])  # Adjust as necessary

                # Create and save the Player with lat/lon=None and district=False
                player = Player(
                    first_name=row['Player First Name'],
                    last_name=row['Player Last Name'],
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    team=team,  
                    latitude=None,
                    longitude=None,
                    district=False  # Explicitly set district to False when geocoding fails
                )
                player.save()
                failed_geocoding.append(address) 
                print(f"Geocoding failed for {address} after {max_retries} retries.")

        # After processing all rows, write the failed addresses to an output.txt file
        if failed_geocoding:
            with open("output.txt", "w") as file:
                file.write("Geocoding failed for the following addresses:\n")
                for address in failed_geocoding:
                    file.write(f"{address}\n")
            print("Failed geocoding addresses have been written to output.txt.")
            return False
        else:
            print("All addresses were successfully geocoded.")
            return True

    def handle(self, *args, **options):
        sleep(5)  # Introduce a time delay before execution
        success = self.import_enrollment_data()
        if success:
            print("Import enrollment data function executed.")
            # Fetch polygons from the KML file
            kml_path = os.path.join(settings.BASE_DIR, 'static', 'District8.kml')
            _, polygons = parse_kml(kml_path)  # Getting only polygons

            players = Player.objects.all()

            for player in players:
                self.stdout.write(f"Checking player: {player.first_name} {player.last_name}")

                # If the player does not have latitude or longitude, set district to False
                if player.latitude is None or player.longitude is None:
                    player.district = False  # Assuming district is a field in the Player model
                    player.save()
                    self.stdout.write(f"Player {player.first_name} {player.last_name} set to outside district due to missing coordinates.")
                else:
                    # Otherwise, check if the player is inside the district
                    check_player_in_district(player, polygons)

            self.stdout.write(self.style.SUCCESS('Successfully updated players with district information'))