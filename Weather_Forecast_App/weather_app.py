import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

API_KEY = "1581a94f1833b5e07d48ad55608c7e32"

def get_weather():
    city = city_var.get()
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
        icon_code = data["weather"][0]["icon"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        country = data["sys"]["country"]

        result = (
            f"📍 City: {city.title()}, {country}\n"
            f"🌤 Weather: {weather}\n"
            f"🌡 Temperature: {temp} °C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind} m/s"
        )
        result_label.config(text=result)

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_img = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather: {e}")

# Draw rounded rectangle
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# GUI Setup
root = tk.Tk()
root.title("🌈 Weather Forecast App")
root.geometry("750x600")
root.config(bg="#eaf6ff")

# Header
header = tk.Label(root, text="🌦 Weather Forecast", font=("Segoe UI", 26, "bold"), bg="#5fa8d3", fg="white", pady=20)
header.pack(fill='x')

# Search Frame (with Canvas)
search_canvas = tk.Canvas(root, width=700, height=100, bg="#eaf6ff", highlightthickness=0)
search_canvas.pack()

# Rounded input background
round_rectangle(search_canvas, 80, 30, 320, 70, radius=20, fill="#ffffff", outline="#ccc")
city_var = tk.StringVar()
city_entry = tk.Entry(root, textvariable=city_var, font=("Segoe UI", 13), bg="#ffffff", bd=0, justify='center')
search_canvas.create_window(200, 50, window=city_entry, width=230, height=30)

# Rounded button background
round_rectangle(search_canvas, 360, 30, 510, 70, radius=20, fill="#1d87e4", outline="")
get_btn = tk.Button(root, text="Get Weather", font=("Segoe UI", 11, "bold"), bg="#1d87e4", fg="white", bd=0,
                    activebackground="#186bb5", activeforeground="white", command=get_weather)
search_canvas.create_window(435, 50, window=get_btn, width=140, height=30)

# Canvas for Result Card
canvas = tk.Canvas(root, width=600, height=300, bg="#eaf6ff", bd=0, highlightthickness=0)
canvas.pack()

# Draw taller rounded rectangle
round_rectangle(canvas, 10, 10, 590, 290, radius=30, fill="white", outline="#cce3f9")

# Embed widgets in result_frame (now vertically centered in taller canvas)
result_frame = tk.Frame(canvas, bg="white")
canvas.create_window(300, 150, window=result_frame)  # y=150 to center in 300 height

icon_label = tk.Label(result_frame, bg="white")
icon_label.pack(pady=(10, 5))

result_label = tk.Label(result_frame, text="", font=("Segoe UI", 14), bg="white", justify="left", fg="#2a2a2a")
result_label.pack(pady=5)


# Footer
footer = tk.Label(root, text="Powered by OpenWeatherMap", font=("Segoe UI", 10), bg="#eaf6ff", fg="#777")
footer.pack(side="bottom", pady=15)

root.mainloop()
