from datetime import datetime
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import polyline
import folium
from folium.features import CustomIcon


auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "117890",
    'client_secret': '6b8d98ed7538ac6c5b006dd4baa1f7356e9b1420',
    'refresh_token': 'b5aa6f285d3b8ce47e8db9532acf942ad2b5267f',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

# Enter the time frame
start_date_str = "2023-04-01" #input("Geben Sie das Startdatum im Format JJJJ-MM-TT ein: ")
end_date_str = "2023-12-06" #input("Geben Sie das Enddatum im Format JJJJ-MM-TT ein: ")
max_activities = 200 #input("Maximale Aktivitäten: ")
start_date = int(datetime.strptime(start_date_str, "%Y-%m-%d").timestamp())
end_date = int(datetime.strptime(end_date_str, "%Y-%m-%d").timestamp())


header = {'Authorization': 'Bearer ' + access_token}
param = {
    "before": end_date,
    "after": start_date,
    "page": 1,
    "per_page": 200
}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

activities_list = []
coords_list = []


m = folium.Map(location=[0, 0], zoom_start=2)

# Extract and store the polylines, names, and dates from each activity
for index, activity in enumerate(my_dataset):
    polyline_str = activity["map"]["summary_polyline"]
    name = activity["name"]
    date = activity["start_date_local"]

    activity_data = {
        "name": name,
        "date": date,
        "polyline": polyline_str
    }

    activities_list.append(activity_data)

    print(f"Name: {name}")
    print(f"Date: {date}")
    print(f"Polyline: {polyline_str}")
    print()  # Add a blank line for separation

    decoded_coords = polyline.decode(polyline_str)

    if len(polyline_str) != 0:
        folium.PolyLine(locations=decoded_coords, color='blue').add_to(m)

file_path = "C:/Users/Public/Documents/map.html"
m.save(file_path)