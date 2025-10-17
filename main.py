from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime, timedelta
import webbrowser
from tkinter import filedialog
from api import fetch_apod

current_date = datetime.today()
def load_apod(date=None):
    global current_date
    data = fetch_apod(date=date.strftime("%Y-%m-%d") if date else None)

    if data is None:
        # Show placeholder image when API fails
        placeholder = Image.new('RGB', (600, 400), color='gray')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder

        title_label.config(text="Offline Mode")
        desc_label.config(text="Could not fetch NASA image. Please check your internet connection.")
        date_label.config(text="")
        video_btn.pack_forget()
        return

    current_date = datetime.strptime(data['date'], "%Y-%m-%d")
    media_type = data['media_type']

    if media_type == 'image':
        img_data = requests.get(data['url']).content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((600, 400))
        tk_img = ImageTk.PhotoImage(img)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = img
        video_btn.pack_forget()  # hide video button if image

    elif media_type == 'video':
        placeholder = Image.new('RGB', (600, 400), color='black')
        tk_img = ImageTk.PhotoImage(placeholder)
        image_label.config(image=tk_img)
        image_label.image = tk_img
        image_label.image_data = placeholder
        video_btn.pack(side=LEFT, padx=5)
        video_btn.url = data['url']

    # Update labels
    title_label.config(text=data['title'])
    desc_label.config(text=data['explanation'])
    date_label.config(text=f"Date: {data['date']}")

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
        #asking path to user for this....
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        if file_path:
            #for saving the given image
            image_label.image_data.save(file_path)
            print(f"Image saved to {file_path}")
    else:
        print("No image to save!")


#most imp giu setupnoe 
root = Tk()
root.title("NASA Astronomy Viewer")
root.geometry("700x700")  # optional window size

top_frame = Frame(root)
top_frame.pack(pady=10)
title_label = Label(top_frame, text="", font=("Arial", 18, "bold"), wraplength=650, justify=CENTER)
title_label.pack()

image_frame = Frame(root)
image_frame.pack(pady=10)
image_label = Label(image_frame)
image_label.pack()

desc_frame = Frame(root)
desc_frame.pack(pady=5)
date_label = Label(desc_frame, text="", font=("Arial", 12))
date_label.pack()
desc_label = Label(desc_frame, text="", wraplength=650, justify=LEFT)
desc_label.pack()

btn_frame = Frame(root)
btn_frame.pack(pady=10)

prev_btn = Button(btn_frame, text="<< Previous", width=12, command=previous_day)
prev_btn.pack(side=LEFT, padx=5)

next_btn = Button(btn_frame, text="Next >>", width=12, command=next_day)
next_btn.pack(side=LEFT, padx=5)

video_btn = Button(btn_frame, text="Watch Video", width=12, command=open_video)
video_btn.pack(side=LEFT, padx=5)

save_btn = Button(btn_frame, text="Save Image", width=12, command=save_image)
save_btn.pack(side=LEFT, padx=5)

retry_btn = Button(btn_frame, text="Retry", width=12, command=lambda: load_apod(current_date))
retry_btn.pack(side=LEFT, padx=5)


#now last load of todays apod by defalut
load_apod()
root.mainloop()
