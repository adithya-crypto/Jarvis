import psutil
import subprocess


def get_cpu_usage():
    """Get current CPU usage percentage."""
    usage = psutil.cpu_percent(interval=1)
    return f"CPU usage is at {usage}%."


def get_memory_usage():
    """Get current RAM usage."""
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024 ** 3)
    total_gb = mem.total / (1024 ** 3)
    return f"Memory usage: {used_gb:.1f} GB of {total_gb:.1f} GB ({mem.percent}%)."


def get_disk_usage():
    """Get disk usage for the main drive."""
    disk = psutil.disk_usage("/")
    used_gb = disk.used / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)
    return f"Disk usage: {used_gb:.0f} GB of {total_gb:.0f} GB used. {free_gb:.0f} GB free ({disk.percent}%)."


def get_battery_status():
    """Get battery info."""
    battery = psutil.sensors_battery()
    if battery:
        status = "charging" if battery.power_plugged else "on battery"
        return f"Battery at {battery.percent}%, {status}."
    return "Battery info not available."


def get_system_summary():
    """Get a full system status summary."""
    parts = [
        get_battery_status(),
        get_cpu_usage(),
        get_memory_usage(),
        get_disk_usage(),
    ]
    return " ".join(parts)


def get_active_app():
    """Get the currently active application on macOS."""
    try:
        script = 'tell application "System Events" to get name of first application process whose frontmost is true'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True
        )
        app_name = result.stdout.strip()
        return f"Currently active app: {app_name}."
    except Exception:
        return "Could not determine the active app."
