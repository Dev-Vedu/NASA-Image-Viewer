from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import os
from datetime import datetime, timedelta
import webbrowser
from api import fetch_apod  #for key

#global
current_date = datetime.today()
current_apod_data = None
FAV_FILE = "favorites.json"

#all type of fun
def load_apod(date=None):
    global current_date, current_apod_data
    data = fetch_apod(date=date.strftime("%Y-%m-%d") if date else None)
    current_apod_data = data

    #by defalut hide btn
    video_btn.pack_forget()
    save_video_btn.pack_forget()

    if data is None:
        placeholder = Image.new('RGB', (600, 400), color='gray')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder

        title_label.config(text="Offline Mode")
        desc_text.delete(1.0, END)
        desc_text.insert(END, "Could not fetch NASA image. Please check your internet connection.")
        date_label.config(text="")
        return

    current_date = datetime.strptime(data['date'], "%Y-%m-%d")
    media_type = data['media_type']

    if media_type == 'image':
        img_data = requests.get(data['url']).content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((650, 400))
        tk_img = ImageTk.PhotoImage(img)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = img

    elif media_type == 'video':
        placeholder = Image.new('RGB', (600, 400), color='black')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder
        video_btn.pack(side=LEFT, padx=5)
        save_video_btn.pack(side=LEFT, padx=5)
        video_btn.url = data['url']

    #label up
    title_label.config(text=data['title'])
    date_label.config(text=f"Date: {data['date']}")
    desc_text.delete(1.0, END)
    desc_text.insert(END, data['explanation'])

def previous_day():
    global current_date
    prev_date = current_date - timedelta(days=1)
    load_apod(prev_date)

def next_day():
    global current_date
    next_date = current_date + timedelta(days=1)
    if next_date <= datetime.today():
        load_apod(next_date)

def open_video():
    url = video_btn.url
    webbrowser.open(url)

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
        messagebox.showwarning("No Image", "No image available to save!")

def save_video(url):
    try:
        video_data = requests.get(url, stream=True, timeout=10)
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            for chunk in video_data.iter_content(1024):
                f.write(chunk)
        messagebox.showinfo("Saved", f"Video saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save video: {e}")

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

    favorites = []
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r") as f:
            try:
                favorites = json.load(f)
            except json.JSONDecodeError:
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
        messagebox.showinfo("No Favorites", "No favorites saved yet!")
        return

    with open(FAV_FILE, "r") as f:
        try:
            favorites = json.load(f)
        except json.JSONDecodeError:
            favorites = []

    if not favorites:
        messagebox.showinfo("Favorites Empty", "Favorites list is empty!")
        return

    fav_window = Toplevel(root)
    fav_window.title("⭐ Your Favorites")
    fav_window.configure(bg="#121212")

    Label(fav_window, text="Your Saved NASA Images", font=("Arial", 14, "bold"), bg="#121212", fg="white").pack(pady=10)

    for fav in favorites:
        frame = Frame(fav_window, bg="#121212")
        frame.pack(fill=X, padx=10, pady=2)

        Label(frame, text=f"{fav['date']} - {fav['title']}", wraplength=400, justify=LEFT, bg="#121212", fg="white").pack(side=LEFT)

        Button(frame, text="Open", command=lambda d=fav['date']: load_apod(datetime.strptime(d, "%Y-%m-%d"))).pack(side=RIGHT, padx=5)

def download_all_favorites():
    if not os.path.exists(FAV_FILE):
        messagebox.showinfo("No Favorites", "You haven't saved any favorites yet!")
        return

    with open(FAV_FILE, "r") as f:
        try:
            favorites = json.load(f)
        except json.JSONDecodeError:
            favorites = []

    if not favorites:
        messagebox.showinfo("No Favorites", "Favorites list is empty!")
        return

    folder = filedialog.askdirectory(title="Select Folder to Save All Favorites")
    if not folder:
        return

    downloaded = 0
    failed = 0

    for fav in favorites:
        url = fav.get("url")
        media_type = fav.get("media_type")
        date = fav.get("date")

        if not url:
            failed += 1
            continue

        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            ext = ".jpg" if media_type == "image" else ".mp4"
            filename = f"{date}_{fav.get('title','nasa_apod').replace(' ','_')}{ext}"
            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            downloaded += 1

        except:
            failed += 1

    messagebox.showinfo("Download Complete",
                        f"✅ Downloaded: {downloaded}\n❌ Failed: {failed}\nSaved to: {folder}")

#giu setup
root = Tk()
root.title("NASA Astronomy Viewer")
root.geometry("700x700")
root.configure(bg="#121212")  # dark theme

#title
top_frame = Frame(root, bg="#121212")
top_frame.pack(pady=10)
title_label = Label(top_frame, text="", font=("Arial", 18, "bold"), wraplength=650, justify=CENTER, bg="#121212", fg="white")
title_label.pack()

#search by date
Label(root, text="Enter Date (YYYY-MM-DD):", font=("Arial", 10), bg="#121212", fg="white").pack(pady=5)
date_entry = Entry(root, width=20, bg="#1e1e1e", fg="white", insertbackground="white")
date_entry.pack(pady=5)
Button(root, text="Search", command=lambda: search_by_date(), bg="#1e1e1e", fg="white").pack(pady=5)

def search_by_date():
    date_str = date_entry.get().strip()
    if not date_str:
        messagebox.showerror("Error", "Please enter a date!")
        return
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj > datetime.today():
            messagebox.showerror("Error", "You cannot select a future date!")
            return
        if date_obj < datetime(1995,6,16):
            messagebox.showerror("Error", "Date must be after June 16, 1995!")
            return
        load_apod(date_obj)
    except:
        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")

#img display
image_frame = Frame(root, bg="#121212")
image_frame.pack(pady=10)
image_label = Label(image_frame, bg="#121212")
image_label.pack()

#scroll the info
desc_frame = Frame(root, bg="#121212")
desc_frame.pack(pady=5, fill=BOTH, expand=True)
scrollbar = Scrollbar(desc_frame, bg="#1e1e1e", troughcolor="#333333")
scrollbar.pack(side=RIGHT, fill=Y)
desc_text = Text(desc_frame, wrap=WORD, yscrollcommand=scrollbar.set, height=8, bg="#1e1e1e", fg="white", insertbackground="white")
desc_text.pack(fill=BOTH, expand=True)
scrollbar.config(command=desc_text.yview)

date_label = Label(desc_frame, text="", font=("Arial",12), bg="#121212", fg="white")
date_label.pack()

#allined
btn_frame = Frame(root, bg="#121212")
btn_frame.pack(pady=15)

#nav btn
nav_frame = Frame(btn_frame, bg="#121212")
nav_frame.grid(row=0, column=0, pady=5)
Button(nav_frame, text="<< Previous", width=12, command=previous_day, bg="#1e1e1e", fg="white").pack(side=LEFT, padx=5)
Button(nav_frame, text="Next >>", width=12, command=next_day, bg="#1e1e1e", fg="white").pack(side=LEFT, padx=5)
Button(nav_frame, text="Retry", width=12, command=lambda: load_apod(current_date), bg="#1e1e1e", fg="white").pack(side=LEFT, padx=5)

#save btn
save_frame = Frame(btn_frame, bg="#121212")
save_frame.grid(row=1, column=0, pady=5)
save_btn = Button(save_frame, text="Save Image", width=12, command=save_image, bg="#1e1e1e", fg="white")
save_btn.pack(side=LEFT, padx=5)
video_btn = Button(save_frame, text="Watch Video", width=12, command=open_video, bg="#1e1e1e", fg="white")
video_btn.pack(side=LEFT, padx=5)
save_video_btn = Button(save_frame, text="Save Video", width=12, command=lambda: save_video(video_btn.url), bg="#1e1e1e", fg="white")
save_video_btn.pack(side=LEFT, padx=5)

#fav 
fav_frame = Frame(btn_frame, bg="#121212")
fav_frame.grid(row=2, column=0, pady=5)
Button(fav_frame, text="⭐ Add to Favorites", width=15, command=add_to_favorites, bg="#1e1e1e", fg="white").pack(side=LEFT, padx=5)
Button(fav_frame, text="🪐 View Favorites", width=15, command=view_favorites, bg="#1e1e1e", fg="white").pack(side=LEFT, padx=5)
download_all_btn = Button(fav_frame, text="⬇️ Download All Favorites", width=20, command=download_all_favorites, bg="#1e1e1e", fg="white")
download_all_btn.pack(side=LEFT, padx=5)

#from today APOD
load_apod()
root.mainloop()
