import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# ------------------ API KEY ------------------
API_KEY = "b7b587e1474ae0355f1e008c42c23971"

# ------------------ APP WINDOW ------------------
app = tk.Tk()
app.title("Weather App")
app.geometry("450x550")
app.config(bg="#87CEEB")

# ------------------ PLACEHOLDER FUNCTIONS ------------------
def clear_placeholder(event):
    if city_entry.get() == "Enter the city name":
        city_entry.delete(0, tk.END)
        city_entry.config(fg="black")

def add_placeholder(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter the city name")
        city_entry.config(fg="grey")

# ------------------ WEATHER FUNCTIONS ------------------
def get_location_by_ip():
    try:
        response = requests.get("https://ipinfo.io/json")
        return response.json().get("city")
    except:
        return None

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def show_weather():
    city = city_entry.get()

    if city == "Enter the city name":
        city = ""

    if city == "":
        city = get_location_by_ip()
        if not city:
            messagebox.showerror("Error", "Location not detected")
            return

    data = fetch_weather(city)

    if data.get("cod") != "200":
        messagebox.showerror("Error", "City not found")
        return

    current = data["list"][0]
    temp = current["main"]["temp"]
    desc = current["weather"][0]["description"].title()
    wind = current["wind"]["speed"]
    icon_code = current["weather"][0]["icon"]

    weather_label.config(
        text=f"📍 {city}\n🌡️ {temp}°C\n☁️ {desc}\n💨 Wind: {wind} m/s"
    )

    load_icon(icon_code)

def load_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    image_data = requests.get(icon_url).content
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    icon_label.config(image=photo)
    icon_label.image = photo

# ------------------ UI COMPONENTS ------------------
title = tk.Label(
    app,
    text="🌦️ Weather App",
    font=("Arial", 18, "bold"),
    bg="#87CEEB"
)
title.pack(pady=10)

city_entry = tk.Entry(app, font=("Arial", 14), fg="grey")
city_entry.pack(pady=5)
city_entry.insert(0, "Enter the city name")

city_entry.bind("<FocusIn>", clear_placeholder)
city_entry.bind("<FocusOut>", add_placeholder)

get_weather_btn = tk.Button(
    app,
    text="Get Weather",
    font=("Arial", 12),
    command=show_weather
)
get_weather_btn.pack(pady=10)

weather_label = tk.Label(
    app,
    font=("Arial", 12),
    bg="#87CEEB"
)
weather_label.pack(pady=10)

icon_label = tk.Label(app, bg="#87CEEB")
icon_label.pack()

# ------------------ RUN APP ------------------
app.mainloop()