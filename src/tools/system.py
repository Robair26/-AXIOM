import os
import subprocess
import psutil

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (f"CPU is at {cpu}% usage. "
            f"Memory is at {memory.percent}% used, "
            f"{round(memory.available / (1024**3), 1)} gigabytes available. "
            f"Disk is at {disk.percent}% full, "
            f"{round(disk.free / (1024**3), 1)} gigabytes free.")

def open_application(app_name):
    apps = {
        "firefox": "firefox",
        "browser": "firefox",
        "chrome": "google-chrome",
        "terminal": "gnome-terminal",
        "files": "nautilus",
        "vscode": "code",
        "vs code": "code",
        "calculator": "gnome-calculator",
        "settings": "gnome-control-center",
        "text editor": "gedit",
    }
    app_name = app_name.lower()
    for key in apps:
        if key in app_name:
            try:
                subprocess.Popen([apps[key]])
                return f"Opening {key} for you."
            except Exception as e:
                return f"Could not open {key}: {str(e)}"
    return f"I don't know how to open {app_name} yet."

def create_folder(folder_name):
    try:
        path = os.path.expanduser(f"~/{folder_name}")
        os.makedirs(path, exist_ok=True)
        return f"Folder {folder_name} created in your home directory."
    except Exception as e:
        return f"Could not create folder: {str(e)}"

def list_files(directory="~"):
    try:
        path = os.path.expanduser(directory)
        files = os.listdir(path)
        return f"Files in {directory}: {', '.join(files[:10])}"
    except Exception as e:
        return f"Could not list files: {str(e)}"

def control_volume(action):
    try:
        if "up" in action or "increase" in action:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
            return "Volume increased."
        elif "down" in action or "decrease" in action:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
            return "Volume decreased."
        elif "mute" in action:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "toggle"])
            return "Volume toggled."
    except Exception as e:
        return f"Volume control failed: {str(e)}"
