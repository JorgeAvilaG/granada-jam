import os
import time
from datetime import datetime
import googlemaps

delta_time = 120 # seconds between measurements
total_time = 3 # total time measurering (hours)
n = int(total_time*60*60/delta_time) # iterations in the for
#n = 1 #test

# Initialize the Google Maps client with your API key
GM_KEY = os.getenv("GM_KEY")
ORIGIN = os.getenv("ORIGIN")
DESTINY = os.getenv("DESTINY")
way1 = os.getenv("WAY1")
way2 = os.getenv("WAY2")
way3 = os.getenv("WAY3")
way4 = os.getenv("WAY4")
way5 = os.getenv("WAY5")

gmaps = googlemaps.Client(key=GM_KEY)
waypoints = [f'via:{way1}', f'via:{way2}', f'via:{way3}', f'via:{way4}', f'via:{way5}']

# Function to get travel time with traffic
def get_directions_with_traffic(origin, destination, waypoints = None, mode='driving'):
    # Get the current time for real-time traffic
    now = datetime.now()
    # Request directions data
    directions_result = gmaps.directions(origin,
                                         destination,
                                         waypoints = waypoints,
                                         mode=mode,
                                         departure_time=now,  # Use current time for traffic info
                                         traffic_model='best_guess')  # Traffic prediction model
    # Extract duration in traffic from the directions result
    duration_in_traffic = directions_result[0]['legs'][0]['duration_in_traffic']['text']
    distance = directions_result[0]['legs'][0]['distance']['text']
    print(f"Estimated travel time (with traffic): {duration_in_traffic}")
    print(f"Distance: {distance}")
    # return duration in seconds, and distance in m
    return now, directions_result[0]['legs'][0]['duration_in_traffic']['value'], directions_result[0]['legs'][0]['distance']['value']
    
        


# Get current date and time
current_date = datetime.now().strftime("%Y-%m-%d")

# Base filename with the current date
file_index = 1
filename = f'log_{current_date}_{file_index}.csv'

# Check if the file already exists
while os.path.exists(filename):
    # If the file exists, add an incrementing index (_2, _3, ...)
    file_index += 1
    filename = f'log_{current_date}_{file_index}.csv'
    

# Write to the file with headers
with open(filename, 'w') as f:
    # Write the headers
    f.write('date,travel_time,distance\n')

f = open(filename,'a')
for _ in range(n):
    try:
        date, travel_time, distance = get_directions_with_traffic(ORIGIN, DESTINY, waypoints = waypoints)
        print(_, date, travel_time, distance)
        f.write(f'{date}, {travel_time}, {distance/1000}\n')
    except:
        print('API error!')
    time.sleep(delta_time)
f.close()

