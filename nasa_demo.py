from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

API_KEY = 'DEMO_KEY'
url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'
response = requests.get(url).json()
img_url = response['url']

img_data = requests.get(img_url).content
img = Image.open(BytesIO(img_data))

root = Tk()
root.title(response['title'])
tk_img = ImageTk.PhotoImage(img)
label = Label(root, image=tk_img)
label.pack()
root.mainloop()
