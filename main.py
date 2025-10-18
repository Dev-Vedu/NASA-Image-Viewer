from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import os
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog
import webbrowser
from api import fetch_apod
#global things
FAV_FILE = "favorites.json"
current_date = datetime.today()
current_apod_data = None
#core needed
def load_apod(date=None):
    global current_date, current_apod_data
    data = fetch_apod(date=date.strftime("%Y-%m-%d") if date else None)
    current_apod_data = data

    #by defalut hide the button
    video_btn.pack_forget()
    save_video_btn.pack_forget()

    if data is None:
        #offline 
        placeholder = Image.new('RGB', (600, 400), color='gray')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder

        title_label.config(text="Offline Mode")
        desc_label.config(text="Could not fetch NASA image. Please check your internet connection.")
        date_label.config(text="")
        return

    current_date = datetime.strptime(data['date'], "%Y-%m-%d")
    media_type = data['media_type']

    #handle the image
    if media_type == 'image':
        img_data = requests.get(data['url']).content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((600, 400))
        tk_img = ImageTk.PhotoImage(img)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = img
        
    if media_type == "video":
        image_label.config(image="")  
        image_label.image = None

        #video btn
        video_btn.pack(side=LEFT, padx=5)
        save_video_btn.pack(side=LEFT, padx=5)

        #url store
        video_url = data["url"]

        def open_video():
            webbrowser.open(video_url)

        def save_video_link():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )
            if file_path:
                with open(file_path, "w") as f:
                    f.write(video_url)
                messagebox.showinfo("Saved", "Video link saved successfully!")

        video_btn.config(command=open_video)
        save_video_btn.config(command=save_video_link)


    #for video
    elif media_type == 'video':
        placeholder = Image.new('RGB', (600, 400), color='black')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder

        video_btn.pack(side=LEFT, padx=5)
        save_video_btn.pack(side=LEFT, padx=5)
        video_btn.url = data['url']

    #update
    title_label.config(text=data['title'])
    desc_label.config(text=data['explanation'])
    date_label.config(text=f"Date: {data['date']}")

#date realated
def previous_day():
    global current_date
    prev_date = current_date - timedelta(days=1)
    load_apod(prev_date)

def next_day():
    global current_date
    next_date = current_date + timedelta(days=1)
    if next_date <= datetime.today():
        load_apod(next_date)

#by dates
def search_by_date():
    date_str = date_entry.get().strip()
    if not date_str:
        messagebox.showerror("Error", "Please enter a date!")
        return

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()

        #not valid future dates
        if date_obj > today:
            messagebox.showerror("Error", "You cannot select a future date!")
            return

        #st-ed at this date
        min_date = datetime(1995, 6, 16)
        if date_obj < min_date:
            messagebox.showerror("Error", "Date must be after June 16, 1995!")
            return

        load_apod(date_obj)

    except ValueError:
        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")

#save option
def open_video():
    url = video_btn.url
    webbrowser.open(url)

def save_video(url):
    try:
        video_data = requests.get(url, stream=True)
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            for chunk in video_data.iter_content(1024):
                f.write(chunk)
        messagebox.showinfo("Saved", f"Video saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save video: {e}")

def save_image():
    if hasattr(image_label, 'image_data'):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        if file_path:
            image_label.image_data.save(file_path)
            messagebox.showinfo("Saved", f"Image saved to {file_path}")
    else:
        messagebox.showwarning("No Image", "No image to save!")

#fav btn
def add_to_favorites():
    if not current_apod_data:
        messagebox.showwarning("No Data", "Please load an image or video first!")
        return

    new_fav = {
        "date": current_apod_data.get("date"),
        "title": current_apod_data.get("title"),
        "url": current_apod_data.get("url"),
        "media_type": current_apod_data.get("media_type"),
        "explanation": current_apod_data.get("explanation")
    }

    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r") as f:
            try:
                favorites = json.load(f)
            except json.JSONDecodeError:
                favorites = []
    else:
        favorites = []

    if any(fav["date"] == new_fav["date"] for fav in favorites):
        messagebox.showinfo("Already Added", "This APOD is already in your favorites!")
        return

    favorites.append(new_fav)
    with open(FAV_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

    messagebox.showinfo("Success", f"Added '{new_fav['title']}' to favorites!")

def view_favorites():
    if not os.path.exists(FAV_FILE):
        messagebox.showinfo("No Favorites", "You have no favorites yet!")
        return

    with open(FAV_FILE, "r") as f:
        favorites = json.load(f)

    if not favorites:
        messagebox.showinfo("Empty", "Your favorites list is empty!")
        return

    fav_window = Toplevel(root)
    fav_window.title("⭐ Your Favorites")

    Label(fav_window, text="Your Saved NASA APODs", font=("Arial", 14, "bold")).pack(pady=10)

    for fav in favorites:
        frame = Frame(fav_window)
        frame.pack(fill=X, padx=10, pady=2)

        Label(frame, text=f"{fav['date']} - {fav['title']}", wraplength=400, justify=LEFT).pack(side=LEFT)
        Button(frame, text="Open", command=lambda d=fav['date']: load_apod(datetime.strptime(d, "%Y-%m-%d"))).pack(side=RIGHT, padx=5)

#imp giu
root = Tk()
root.title("NASA Astronomy Viewer")
root.geometry("700x700")

#title
top_frame = Frame(root)
top_frame.pack(pady=10)
title_label = Label(top_frame, text="", font=("Arial", 18, "bold"), wraplength=650, justify=CENTER)
title_label.pack()

#by date search
Label(root, text="Enter Date (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
date_entry = Entry(root, width=20)
date_entry.pack(pady=5)
Button(root, text="Search", command=search_by_date).pack(pady=5)

#display img
image_frame = Frame(root)
image_frame.pack(pady=10)
image_label = Label(image_frame)
image_label.pack()

#info of image
desc_frame = Frame(root)
desc_frame.pack(pady=5)
date_label = Label(desc_frame, text="", font=("Arial", 12))
date_label.pack()
desc_label = Label(desc_frame, text="", wraplength=650, justify=LEFT)
desc_label.pack()

#aligned btn
btn_frame = Frame(root)
btn_frame.pack(pady=15)

#nav btn
nav_frame = Frame(btn_frame)
nav_frame.grid(row=0, column=0, pady=5)
Button(nav_frame, text="<< Previous", width=12, command=previous_day).pack(side=LEFT, padx=5)
Button(nav_frame, text="Next >>", width=12, command=next_day).pack(side=LEFT, padx=5)
Button(nav_frame, text="Retry", width=12, command=lambda: load_apod(current_date)).pack(side=LEFT, padx=5)

#save btn
save_frame = Frame(btn_frame)
save_frame.grid(row=1, column=0, pady=5)
Button(save_frame, text="Save Image", width=12, command=save_image).pack(side=LEFT, padx=5)
video_btn = Button(save_frame, text="Watch Video", width=12, command=open_video)
video_btn.pack(side=LEFT, padx=5)
save_video_btn = Button(save_frame, text="Save Video", width=12, command=lambda: save_video(video_btn.url))
save_video_btn.pack(side=LEFT, padx=5)

#fav btn
fav_frame = Frame(btn_frame)
fav_frame.grid(row=2, column=0, pady=5)
Button(fav_frame, text="⭐ Add to Favorites", width=15, command=add_to_favorites).pack(side=LEFT, padx=5)
Button(fav_frame, text="🪐 View Favorites", width=15, command=view_favorites).pack(side=LEFT, padx=5)

#today 
load_apod()
root.mainloop()
