import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

API_KEY = "1581a94f1833b5e07d48ad55608c7e32"
dark_mode = False

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

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg_color = "#121212" if dark_mode else "#eaf6ff"
    fg_color = "#f5f5f5" if dark_mode else "#2a2a2a"
    card_bg = "#1e1e1e" if dark_mode else "white"
    border_color = "#444" if dark_mode else "#cce3f9"
    btn_bg = "#333" if dark_mode else "#1d87e4"
    footer_fg = "#aaa" if dark_mode else "#777"
    entry_bg = "#1e1e1e" if dark_mode else "#ffffff"

    root.config(bg=bg_color)
    header.config(bg="#5fa8d3", fg="white")
    footer.config(bg=bg_color, fg=footer_fg)

    search_canvas.config(bg=bg_color)
    search_canvas.delete("all")

    round_rectangle(search_canvas, 80, 30, 320, 70, radius=20, fill=entry_bg, outline=border_color)
    search_canvas.create_window(200, 50, window=city_entry, width=230, height=30)

    round_rectangle(search_canvas, 360, 30, 510, 70, radius=20, fill=btn_bg, outline="")  # Rounded Button
    search_canvas.create_window(435, 50, window=get_btn, width=140, height=30)

    city_entry.config(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    get_btn.config(bg=btn_bg, fg="white", activebackground=btn_bg)

    canvas.config(bg=bg_color)
    canvas.delete("all")

    round_rectangle(canvas, 10, 10, 590, 440, radius=30, fill=card_bg, outline=border_color)
    canvas.create_window(300, 225, window=result_frame)

    result_frame.config(bg=card_bg)
    result_label.config(bg=card_bg, fg=fg_color)
    icon_label.config(bg=card_bg)

    toggle_canvas.config(bg=bg_color)
    draw_toggle()

# GUI
root = tk.Tk()
root.title("🌈 Weather Forecast App")
root.geometry("750x700")
root.config(bg="#eaf6ff")

header = tk.Label(root, text="🌦 Weather Forecast", font=("Segoe UI", 26, "bold"), pady=20)
header.pack(fill='x')

# Search section
search_canvas = tk.Canvas(root, width=700, height=100, highlightthickness=0, bg="#eaf6ff")
search_canvas.pack()

city_var = tk.StringVar()
city_entry = tk.Entry(root, textvariable=city_var, font=("Segoe UI", 13), bd=0, justify='center')
get_btn = tk.Button(root, text="Get Weather", font=("Segoe UI", 11, "bold"), bd=0, command=get_weather)

# Theme Toggle Switch
def draw_toggle():
    toggle_canvas.delete("all")
    bg = "#4a4a4a" if dark_mode else "#ddd"
    knob_pos = (32, 2, 58, 28) if dark_mode else (2, 2, 28, 28)
    emoji_pos = (10, 15) if dark_mode else (50, 15)
    emoji = "🌙" if dark_mode else "☀️"
    emoji_color = "white" if dark_mode else "black"

    # Rounded switch background
    toggle_canvas.create_oval(0, 0, 30, 30, fill=bg, outline=bg)
    toggle_canvas.create_oval(30, 0, 60, 30, fill=bg, outline=bg)
    toggle_canvas.create_rectangle(15, 0, 45, 30, fill=bg, outline=bg)

    # Knob
    toggle_canvas.create_oval(*knob_pos, fill="#ffffff", outline="#cccccc")

    # Emoji
    toggle_canvas.create_text(*emoji_pos, text=emoji, fill=emoji_color, font=("Segoe UI", 10, "bold"))

def toggle_theme_switch(event=None):
    toggle_theme()

toggle_canvas = tk.Canvas(root, width=60, height=30, highlightthickness=0, bg="#eaf6ff")
toggle_canvas.pack(pady=5)
toggle_canvas.bind("<Button-1>", toggle_theme_switch)

# Info Card
canvas = tk.Canvas(root, width=600, height=450, bd=0, highlightthickness=0)
canvas.pack()

result_frame = tk.Frame(canvas, bg="white")
icon_label = tk.Label(result_frame, bg="white")
icon_label.pack(pady=(10, 5))

result_label = tk.Label(result_frame, text="", font=("Segoe UI", 14), bg="white", justify="left", fg="#2a2a2a")
result_label.pack(pady=5)

footer = tk.Label(root, text="Powered by OpenWeatherMap", font=("Segoe UI", 10), fg="#777")
footer.pack(side="bottom", pady=15)

# Initial styling
apply_theme()
root.mainloop()
