📝 Task Logger with GUI, Reminders & Productivity Stats
A Python-based desktop app to log tasks, receive timed reminders via system notifications, track daily activity, and visualize weekly productivity—all with a clean graphical interface.

🚀 Features
⏰ Custom Reminder Interval – Get notified every X minutes to log what you've done

🗂 Daily CSV File Logging – Tasks are stored per day as tasks_YYYY-MM-DD.csv

📊 Stats Dashboard – View summary of today’s progress at a click

📈 Weekly Graphs – Visualize how active you've been with Matplotlib

🖥 System Tray Integration – Runs in the background with a tray icon

📦 Single Executable Buildable – Can be packaged to run without Python

📂 Folder Structure
task-tracker/
│
├── task_logger.py         # Main application
├── tasks_YYYY-MM-DD.csv   # Auto-generated task logs per day
├── README.md              # You're reading this
🛠 Requirements
Install dependencies with:

bash
pip install matplotlib pystray pillow plyer
Make sure Python 3.9–3.12 is used for compatibility with PyInstaller packaging.

🧪 How to Run
bash
python task_logger.py
If you'd prefer packaging it into a standalone .exe:

bash
pyinstaller --onefile --windowed task_logger.py
(Recommend using Python ≤ 3.12 for packaging due to bytecode compatibility)

📉 Example Output
CSV Log Example:

Date,Time,Task
2024-06-24,09:00,Reviewed PRs
2024-06-24,10:00,Debugged login feature
Weekly Productivity Graph: Bar chart of task counts for each of the past 7 days

💡 Inspiration
Created to help stay accountable, fight context-switching fatigue, and track real, bite-sized progress without drowning in productivity tools.
