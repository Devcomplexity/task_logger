import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import threading
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pystray import Icon as TrayIcon, MenuItem as item
from PIL import Image, ImageDraw
import winsound  # for audible beeps on Windows

class TaskLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Logger")
        self.running = False
        self.interval = 60  # default reminder interval in minutes
        self.csv_file = "tasks.csv"
        self.init_storage()
        self.create_widgets()
        self.tray_icon = None
        self.start_tray_icon()
        # Initialize timer variables
        self.remaining_time = self.interval * 60  # countdown in seconds
        self.timer_label = ttk.Label(self.root, text="", font=("Segoe UI", 12))
        self.timer_label.pack(pady=5)
        self.update_timer()  # start the timer update loop

    def init_storage(self):
        """Create the CSV file if it doesn't already exist, with a header."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Task"])

    def create_widgets(self):
        """Configure the main GUI components."""
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Reminder Interval (minutes):").grid(row=0, column=0, sticky="w")
        self.interval_entry = ttk.Entry(frame, width=10)
        self.interval_entry.insert(0, "60")
        self.interval_entry.grid(row=0, column=1, sticky="w", padx=5)

        start_button = ttk.Button(frame, text="Start Tracking", command=self.start_tracking)
        start_button.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame, text="Enter Task:").grid(row=1, column=0, sticky="w", pady=5)
        self.task_entry = ttk.Entry(frame, width=50)
        self.task_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

        save_button = ttk.Button(frame, text="Save Task", command=self.save_task)
        save_button.grid(row=1, column=3, padx=5, pady=5)

        stats_button = ttk.Button(frame, text="Show Daily Stats", command=self.show_daily_stats)
        stats_button.grid(row=2, column=0, padx=5, pady=5)

        graph_button = ttk.Button(frame, text="Show Weekly Graph", command=self.show_weekly_graph)
        graph_button.grid(row=2, column=1, padx=5, pady=5)

        quit_button = ttk.Button(frame, text="Quit", command=self.quit_app)
        quit_button.grid(row=2, column=2, padx=5, pady=5)

    def save_task(self):
        """Save the current task input into the CSV file."""
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Empty Input", "Please enter a task before saving.")
            return
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date_str, time_str, task])
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Task Saved", f"Task logged at {time_str}")

    def start_tracking(self):
        """Start tracking and initialize the countdown timer."""
        try:
            self.interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for minutes.")
            return
        self.running = True
        self.remaining_time = self.interval * 60  # reset countdown based on the new interval
        messagebox.showinfo("Tracking Started", f"Reminders set for every {self.interval} minutes.")

    def update_timer(self):
        """Update the visual countdown timer and trigger the alarm when time is up."""
        if self.running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"⏳ Next reminder in {mins:02}:{secs:02}")
            if self.remaining_time > 0:
                self.remaining_time -= 1
            else:
                self.trigger_alarm()
                self.remaining_time = self.interval * 60  # restart the countdown
        else:
            self.timer_label.config(text="⏹ Tracking paused")
        self.root.after(1000, self.update_timer)

    def trigger_alarm(self):
        """Play a sound and show a popup alert as an alarm."""
        winsound.Beep(1000, 700)  # Beep at 1000Hz for 700ms
        messagebox.showinfo("⏰ Reminder", "It's time to log your task!")

    def show_daily_stats(self):
        """Read today's tasks from the CSV and display a summary."""
        today = datetime.now().strftime("%Y-%m-%d")
        tasks_today = []
        with open(self.csv_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row in reader:
                if len(row) >= 3 and row[0] == today:
                    tasks_today.append(row)
        count = len(tasks_today)
        stats_message = f"Tasks for {today}: {count}\n"
        for task in tasks_today:
            stats_message += f"{task[1]} - {task[2]}\n"
        messagebox.showinfo("Daily Stats", stats_message)

    def show_weekly_graph(self):
        """Aggregate tasks for the last 7 days and plot a bar chart."""
        dates = {}
        today_date = datetime.now().date()
        for i in range(7):
            day = today_date - timedelta(days=i)
            dates[day.strftime("%Y-%m-%d")] = 0
        
        with open(self.csv_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    date_str = row[0]
                    if date_str in dates:
                        dates[date_str] += 1

        sorted_dates = sorted(dates.keys())
        counts = [dates[d] for d in sorted_dates]

        plt.figure(figsize=(8, 4))
        plt.bar(sorted_dates, counts, color="skyblue")
        plt.xlabel("Date")
        plt.ylabel("Number of Tasks")
        plt.title("Tasks Logged in the Past Week")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def create_tray_image(self):
        """Creates a simple tray icon image using Pillow."""
        image = Image.new("RGB", (64, 64), color="white")
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill="black")
        return image

    def start_tray_icon(self):
        """Start the system tray icon (with a Quit menu) in a separate thread."""
        def setup_tray():
            menu = (item("Quit", lambda _: self.quit_app()),)
            self.tray_icon = TrayIcon("Task Logger", self.create_tray_image(), menu=menu)
            self.tray_icon.run()
        tray_thread = threading.Thread(target=setup_tray, daemon=True)
        tray_thread.start()

    def quit_app(self):
        """Stop background activities, tray icon, and quit the application."""
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

def main():
    root = tk.Tk()
    app = TaskLoggerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()

if __name__ == "__main__":
    main()
