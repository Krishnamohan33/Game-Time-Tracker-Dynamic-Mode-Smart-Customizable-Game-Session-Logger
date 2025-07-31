"""
Game Time Tracker (Dynamic Mode)
© 2025 Krishnamohan Yagneswaran
Custom MIT License • https://github.com/Krishnamohan33/Game-Time-Tracker-Dynamic-Mode-Smart-Customizable-Game-Session-Logger
"""

import tkinter as tk
import psutil
import sqlite3
import time
import threading
import webbrowser
from datetime import datetime

# === DB SETUP ===
conn = sqlite3.connect("sessions.db", check_same_thread=False)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT,
    start_time TEXT,
    end_time TEXT
)
''')
conn.commit()
active_sessions = {}

# === TRACKED GAME (set later from input) ===
tracked_game = None
DAILY_LIMIT_MINUTES = 120

def log_session(game, start, end):
    cur.execute("INSERT INTO sessions (game, start_time, end_time) VALUES (?, ?, ?)",
                (game, start.isoformat(), end.isoformat()))
    conn.commit()

def tracker_loop():
    while True:
        if not tracked_game:
            time.sleep(3)
            continue
        running = {p.name(): p.pid for p in psutil.process_iter(['name'])}
        if tracked_game in running and tracked_game not in active_sessions:
            active_sessions[tracked_game] = datetime.now()
        elif tracked_game not in running and tracked_game in active_sessions:
            log_session(tracked_game, active_sessions[tracked_game], datetime.now())
            del active_sessions[tracked_game]
        time.sleep(5)

def get_stats(game):
    cur.execute("SELECT game, start_time, end_time FROM sessions WHERE game = ?", (game,))
    sessions = cur.fetchall()
    total = 0
    durations = []

    for _, start, end in sessions:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        delta = (end_dt - start_dt).total_seconds()
        total += delta
        durations.append(delta)

    return {
        "total_hours": round(total / 3600, 2),
        "avg_session": round(sum(durations)/len(durations)/60, 2) if durations else 0
    }

def get_focus_score(game):
    today = datetime.now().date()
    cur.execute("SELECT start_time, end_time FROM sessions WHERE game = ?", (game,))
    sessions = cur.fetchall()
    total_today = 0
    for start, end in sessions:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        if start_dt.date() == today:
            total_today += (end_dt - start_dt).total_seconds()
    total_minutes = total_today / 60
    ratio = total_minutes / DAILY_LIMIT_MINUTES
    if ratio <= 1:
        return round(total_minutes), max(round((1 - ratio) * 100), 0), "#4CAF50"
    elif ratio <= 1.5:
        return round(total_minutes), max(round((1.5 - ratio) * 100), 0), "#FFA500"
    else:
        return round(total_minutes), 0, "#F44336"

def start_tracker_ui(game_name):
    global tracked_game
    tracked_game = game_name

    stats = get_stats(tracked_game)
    today_minutes, score, score_color = get_focus_score(tracked_game)

    app = tk.Tk()
    app.title(f"Tracking: {tracked_game}")
    app.configure(bg="#1e1e1e")
    app.geometry("600x500")
    app.resizable(False, False)

    def add_label(parent, text, size=12, color="#FFFFFF", bold=False, pady=4):
        weight = "bold" if bold else "normal"
        lbl = tk.Label(parent, text=text, font=("Segoe UI", size, weight), fg=color, bg="#1e1e1e")
        lbl.pack(anchor="w", pady=pady)
        return lbl

    frame = tk.Frame(app, bg="#1e1e1e", padx=30, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🎮 Game Time Tracker", font=("Segoe UI", 18, "bold"), fg="#00BFFF", bg="#1e1e1e").pack(anchor="center")
    tk.Label(frame, text=f"Tracking: {tracked_game}", font=("Segoe UI", 12), fg="#AAAAAA", bg="#1e1e1e").pack(anchor="center", pady=(0, 20))

    status_lbl = add_label(frame, f"{tracked_game}: Checking...", bold=True)

    def update_status():
        while True:
            running = {p.name() for p in psutil.process_iter(['name'])}
            running_now = tracked_game in running
            status_lbl.config(
                text=f"{tracked_game}: {'🟢 Running' if running_now else '🔴 Not running'}",
                fg="#4CAF50" if running_now else "#F44336"
            )
            time.sleep(3)

    add_label(frame, f"Total Playtime: {stats['total_hours']} hrs", size=14, bold=True, color="#00FFAA")
    add_label(frame, f"Average Session: {stats['avg_session']} min", size=14, bold=True, color="#00FFAA")

    add_label(frame, f"\nToday's Play Time: {today_minutes} min", size=12, color="#CCCCCC")
    tk.Label(frame, text=f"🌟 Focus Score: {score}", font=("Segoe UI", 16, "bold"), fg=score_color, bg="#1e1e1e").pack(anchor="w", pady=(0, 10))

    # GitHub link label
    def open_github(event):
        webbrowser.open_new("https://github.com/Krishnamohan33/Game-Time-Tracker-Dynamic-Mode-Smart-Customizable-Game-Session-Logger")

    link_label = tk.Label(
        frame,
        text="© 2025 Krishnamohan Yagneswaran • MIT License • GitHub",
        font=("Segoe UI", 9, "underline"),
        fg="#4ea3f1",
        bg="#1e1e1e",
        cursor="hand2"
    )
    link_label.pack(side="bottom", pady=10)
    link_label.bind("<Button-1>", open_github)

    threading.Thread(target=update_status, daemon=True).start()
    app.mainloop()

def entry_screen():
    entry_root = tk.Tk()
    entry_root.title("Enter Game EXE Name")
    entry_root.geometry("400x200")
    entry_root.configure(bg="#1e1e1e")

    tk.Label(entry_root, text="Enter the .exe name of the game to track (e.g., SkyrimSE.exe)", 
             font=("Segoe UI", 11), fg="#00BFFF", bg="#1e1e1e", wraplength=380).pack(pady=20)

    exe_entry = tk.Entry(entry_root, font=("Segoe UI", 12), width=30)
    exe_entry.pack(pady=10)

    def on_submit():
        game = exe_entry.get().strip()
        if game:
            entry_root.destroy()
            threading.Thread(target=tracker_loop, daemon=True).start()
            start_tracker_ui(game)

    tk.Button(entry_root, text="Start Tracking", font=("Segoe UI", 12, "bold"), bg="#00BFFF", fg="#fff",
              activebackground="#009ACD", command=on_submit).pack(pady=10)

    entry_root.mainloop()

if __name__ == "__main__":
    entry_screen()
