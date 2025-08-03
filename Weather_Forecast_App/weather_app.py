import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "1581a94f1833b5e07d48ad55608c7e32" 

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", f"City not found: {city}")
            return

        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        country = data["sys"]["country"]
        result = (
            f"City: {city.title()}\n"
            f"Country: {country}\n"
            f"Weather: {weather}\n"
            f"Temperature: {temp} °C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )
        result_label.config(text=result)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather: {e}")

# GUI setup
root = tk.Tk()
root.title("Weather Forecast App")
root.geometry("850x600")
root.config(bg="#eef5ff")

tk.Label(root, text="Enter City Name:", font=("Arial", 12), bg="#eef5ff").pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 12), justify='center')
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather, bg="#87cefa").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="#eef5ff", justify="left")
result_label.pack(pady=10)

root.mainloop()
