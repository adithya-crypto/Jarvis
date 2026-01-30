import subprocess


def notify(title, message, sound=True):
    """Send a macOS desktop notification using osascript."""
    sound_str = 'sound name "default"' if sound else ""
    script = f'display notification "{message}" with title "{title}" {sound_str}'
    try:
        subprocess.run(["osascript", "-e", script])
        return f"Notification sent: {title}."
    except Exception as e:
        print(f"Notification error: {e}")
        return "Failed to send notification."


def notify_reminder(message):
    """Send a reminder notification."""
    return notify("JARVIS Reminder", message)


def notify_alert(message):
    """Send an alert notification."""
    return notify("JARVIS Alert", message)
