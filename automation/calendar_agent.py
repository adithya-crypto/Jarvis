"""
Calendar Agent - Provides reminders and timer functionality.

Basic timer/reminder support is built-in. For Google Calendar integration,
configure OAuth2 credentials in config/credentials.json.
"""
import threading
import time


_active_timers = {}


def set_reminder(message, minutes):
    """Set a reminder that fires after the specified number of minutes."""
    def _reminder_callback():
        print(f"REMINDER: {message}")
        # The main loop can pick this up for speech output
        _active_timers.pop(message, None)

    timer = threading.Timer(minutes * 60, _reminder_callback)
    timer.daemon = True
    timer.start()
    _active_timers[message] = timer
    return f"Reminder set: '{message}' in {minutes} minutes."


def cancel_reminder(message):
    """Cancel an active reminder."""
    timer = _active_timers.pop(message, None)
    if timer:
        timer.cancel()
        return f"Reminder '{message}' cancelled."
    return "No active reminder found with that description."


def list_reminders():
    """List all active reminders."""
    if not _active_timers:
        return "No active reminders."
    names = ", ".join(_active_timers.keys())
    return f"Active reminders: {names}."


def start_timer(minutes):
    """Start a countdown timer."""
    return set_reminder("Timer complete", minutes)


def check_calendar():
    """Check calendar events. Requires Google Calendar API setup."""
    return ("Calendar integration is not yet configured. "
            "To enable it, set up Google Calendar API credentials in config/credentials.json.")
