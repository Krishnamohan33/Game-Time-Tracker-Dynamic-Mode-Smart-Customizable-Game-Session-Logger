# 🎮 Game Time Tracker (Dynamic Mode)

A lightweight, modern desktop application to help you understand and manage how much time you spend playing your favorite PC games.

Enter your game's `.exe` name (for example, `SkyrimSE.exe`) and the app will automatically detect when the game is running, track your sessions, and give you insights like total playtime, average session length, and a daily focus score.

---

## 💡 Features

- **Dynamic Game Detection**  
  Just enter the game's `.exe` name — no setup files or folders needed.

- **Session Tracking**
  - Automatically logs game start and end times
  - Tracks all sessions locally

- **Usage Analytics**
  - Total hours played
  - Average session duration (in minutes)
  - Daily playtime (in minutes)
  - Smart "Focus Score" based on a 2-hour daily target, with color-coded feedback

- **Modern GUI**
  - Dark mode interface
  - Clean layout with live status updates
  - GitHub and license footer included

---

## ✅ What's Included in Version 1.0

- 🔍 Real-time tracking of any game entered by `.exe` name
- 💾 Local database using SQLite (`sessions.db`)
- 📊 Playtime stats: total hours, average session, daily time
- 🧠 Focus score with health-focused limits
- 🖥️ Clean GUI with responsive updates
- 🔗 Embedded GitHub link and license in footer

---

## 🛠 Tech Stack

- Python 3.10 or higher
- `psutil` – process detection
- `sqlite3` – session data storage
- `tkinter` – GUI interface
- `threading` – background tracking loop

---

## 📚 Understanding the Code

The code is structured to be simple and readable:
- `tracker_loop()` runs continuously and checks if your game is active.
- When a session starts or ends, it logs timestamps to a local SQLite database.
- The GUI updates the session statistics in real-time and displays your current status.
- The focus score helps you monitor how long you’ve played today and gives a green, orange, or red signal based on daily usage.

All logic is commented, and the code is organized in a way that makes it easy to learn from or customize.

---

## 🚀 Usage Instructions

1. Open the application (`main.py`)
2. Enter the name of your game's executable (e.g., `GTA5.exe`)
3. The app will track when the game runs and logs your sessions automatically
4. Your total time, session info, and daily focus score will be displayed in the GUI

To create a standalone `.exe` version, you can use tools like PyInstaller (optional).

---

## 🤝 Contributions & Community

This project is open source and intended to stay free for all users.

You are welcome to:
- Contribute code or ideas
- Suggest improvements
- Support the developer through optional donations

Please do **not**:
- Repackage or resell this app
- Use it commercially without the author's permission

---

## 📄 License

MIT License (Custom Condition: Non-Commercial Use Only)  
© 2025 Krishnamohan Yagneswaran

Permission is granted, free of charge, to use, copy, modify, and distribute this software for **personal and educational use** only.

**Commercial use or resale is strictly prohibited.**

All copies must include this license notice.

---
