🌌 NASA Astronomy Image Viewer
A beautiful desktop application built with Python and Tkinter, using NASA’s Astronomy Picture of the Day (APOD) API.
It allows users to view daily space images, search by date, watch NASA videos, save favorites, and download images/videos locally.

🛰️ Features
✅ Fetch NASA’s APOD (Astronomy Picture of the Day) using official API
✅ Search by Date (view images from any date)
✅ Offline Placeholder (shows message when internet is unavailable)
✅ Favorites System — save your favorite NASA images
✅ Save Image/Video — download directly to your PC
✅ Previous / Next Navigation
✅ Video Support (open YouTube/Vimeo NASA videos)
✅ Clean & Responsive Tkinter UI

🧠 Technologies Used
Component	Description
Python 3	Core programming language
Tkinter	GUI (Graphical User Interface)
Requests	For API and web data fetching
Pillow (PIL)	Image handling and display
NASA APOD API	Astronomy Picture of the Day API

📦 Installation
1️⃣ Clone the Repository
bash
Copy code
git clone https://github.com/Dev-Vedu/NASA-Image-Viewer.git
cd NASA-Image-Viewer
2️⃣ Install Dependencies
bash
Copy code
pip install requests pillow
3️⃣ Get Your NASA API Key
Go to 🔗 https://api.nasa.gov/
Generate your personal API key, then set it as an environment variable:

On Windows PowerShell:
bash
Copy code
$env:NASA_API_KEY="YOUR_API_KEY_HERE"
🚀 Run the Application
bash
Copy code
python main.py
💾 Project Structure
graphql
Copy code
NASA-Image-Viewer/
│
├── api.py              # Handles NASA API calls
├── main.py             # Tkinter GUI + App logic
├── favorites.json      # Stores user favorites
├── README.md           # Documentation
└── requirements.txt    # Python dependencies
🌠 Screenshots
Home Screen	Search by Date	Favorites
(Add screenshots later when you capture them)	(Show how it looks when searching by date)	(Show favorites window)

💡 Future Improvements
Add Dark Mode UI

Add Image Zoom and slideshow feature

Integrate with NASA Mars Rover Photos API

🧑‍🚀 Credits
Developed by Harsha Gorda
API Source: NASA Open APIs

📜 License
This project is licensed under the MIT License — you are free to use, modify, and distribute.

