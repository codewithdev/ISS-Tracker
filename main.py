#Importing libraries
import requests
import tkinter as tk
import folium
from tkinter import Label, StringVar
from folium.plugins import MarkerCluster

def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            iss_position = data["iss_position"]
            latitude = float(iss_position["latitude"])
            longitude = float(iss_position["longitude"])
            return latitude, longitude
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

#Update location function
def update_location():
    location_data = get_iss_location()
    if location_data:
        latitude, longitude = location_data
        location_var.set(f"Latitude: {latitude}, Longitude: {longitude}")

        # Update the map with the new ISS location
        iss_map.location = [latitude, longitude]
        marker = folium.Marker(location=[latitude, longitude], popup="ISS Location")
        marker_cluster.add_child(marker)

    app.after(10000, update_location)  # Update every 10 seconds

# Create the Tkinter window
app = tk.Tk()
app.title("ISS Location Tracker")

# Create a StringVar to store the ISS location data
location_var = StringVar()
location_label = Label(app, textvariable=location_var, font=("Arial", 14))
location_label.pack(pady=20)

# Create a Folium map
iss_map = folium.Map(location=[0, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(iss_map)

# Start fetching the location data and update the Tkinter app window every 10 seconds
update_location()

# Run the Tkinter main loop
app.mainloop()
