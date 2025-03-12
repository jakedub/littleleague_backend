import os
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def import_enrollment_data():
    # Importing models inside the function to avoid circular import issues
    from .models import Player, Team  # Import the Player and Team models inside the function

    # Path to your CSV file, make sure the file is placed correctly (adjust path if needed)
    csv_file_path = os.path.join('static', 'Enrollment Address.csv')

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        print(f"File not found: {csv_file_path}")
        return

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Create an instance of geolocator
    geolocator = Nominatim(user_agent="myApp")

    # List to store failed geocoding addresses
    failed_geocoding = []

    # Retry parameters
    max_retries = 3
    retry_delay = 2  # Seconds to wait between retries

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the necessary fields
        street_address = row['Street Address']
        city = row['City']
        state = row['State']
        postal_code = row['Postal Code']
        
        # Combine the address for geocoding
        address = f"{street_address}, {city}, {state}, {postal_code}"

        print(f"Attempting to geocode: {address}")

        location = None
        retries = 0
        while retries < max_retries and location is None:
            try:
                location = geolocator.geocode(address, timeout=10)  # Increase timeout if needed
                if location:
                    print(f"Geocoding successful for: {address}")
                    break  # Exit loop if geocoding was successful
                else:
                    print(f"Geocoding returned None for {address}")
                    break
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                retries += 1
                print(f"Geocoding failed for {address}. Retrying {retries}/{max_retries}...")
                sleep(retry_delay)  # Wait before retrying
            except Exception as e:
                print(f"Unexpected error occurred for {address}: {e}")
                break  # Exit the loop if an unexpected error happens

        if location:
            # If location found, create or fetch the Team if available
            team_name = row['Program Name']  # Assuming team information exists in the CSV
            team, created = Team.objects.get_or_create(name=team_name, city=row['City'])  # Adjust as necessary

            # Create and save the Player
            player = Player(
                first_name=row['Player First Name'],
                last_name=row['Player Last Name'],
                street_address=street_address,
                city=city,
                state=state,
                postal_code=postal_code,
                team=team,  # Assign the found or created team
                latitude=location.latitude,
                longitude=location.longitude
            )
            player.save()
            print(f"Player {player.first_name} {player.last_name} saved.")
        else:
            # Append the failed geocoding address to the list after max retries
            failed_geocoding.append(address)
            print(f"Geocoding failed for {address} after {max_retries} retries.")

    # After processing all rows, write the failed addresses to an output.txt file
    if failed_geocoding:
        with open("output.txt", "w") as file:
            file.write("Geocoding failed for the following addresses:\n")
            for address in failed_geocoding:
                file.write(f"{address}\n")
        print("Failed geocoding addresses have been written to output.txt.")
    else:
        print("All addresses were successfully geocoded.")


# Call the function to import the data
import_enrollment_data()