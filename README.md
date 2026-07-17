🧺 Hostel Laundry AI - Smart Scheduler

📌 Overview

Hostel Laundry AI is a web-based optimization platform designed to solve the common hostel problem of overcrowded laundry rooms. Instead of students walking back and forth to check machine availability, this platform provides a real-time digital twin of the laundry room.

By combining State Management with Predictive Analytics, the app helps students identify the best time to do their laundry, reducing wait times and improving hostel resource management.
🚀 Live Demo

Check out the live application here:https://hostel-laundary-ai-cn8gdyigdrjdbxxsyp242d.streamlit.app/

👉 Hostel Laundry AI Live
✨ Key Features

    Live Status Dashboard: Real-time visibility into which machines are Available, Busy, or Under Maintenance.

    Intelligent Timers: Active countdowns showing exactly when a machine will be free.

    One-Click Reservation: Simple UI for students to "Claim" a machine and start a session.

    AI Wait-Time Prediction: Estimates the shortest wait time based on active cycles and historical peak-usage data.

    Mobile-First Design: Fully responsive UI built with Streamlit for on-the-go access.

🛠️ Tech Stack

    Frontend: Streamlit (Reactive Python Web Framework)

    Backend: Python (State Logic & Session Management)

    Data Handling: Pandas & NumPy for usage analytics.

    Deployment: Streamlit Cloud.


  🏗️ Project Architecture
  
    ├── app.py                # Main Streamlit application entry point
    ├── logic/
    │   ├── timer_engine.py   # Handles real-time countdowns
    │   └── analytics.py      # Predictive logic for wait times
    ├── data/
    │   └── usage_logs.csv    # (Optional) Historical data for AI trends
    ├── requirements.txt      # Python dependencies
    └── README.md             # Project documentation

  🔮 Future Roadmap

    [ ] IoT Integration: Connecting vibration sensors to automate status updates.

    [ ] User Authentication: Login system for individual student tracking.

    [ ] Notification Bot: WhatsApp/Telegram alerts when a machine becomes free.
