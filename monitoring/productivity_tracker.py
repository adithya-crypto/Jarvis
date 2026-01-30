"""
Productivity Tracker - Tracks app usage time during a session.
"""
import time
import json
import os
import subprocess

TRACKER_FILE = "data/productivity_log.json"


class ProductivityTracker:
    def __init__(self):
        self.session_start = time.time()
        self.app_usage = {}  # {app_name: total_seconds}
        self._last_app = None
        self._last_check = time.time()

    def _get_active_app(self):
        """Get the currently focused application."""
        try:
            script = 'tell application "System Events" to get name of first application process whose frontmost is true'
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except Exception:
            return None

    def tick(self):
        """Call periodically to record which app is active."""
        now = time.time()
        current_app = self._get_active_app()

        if self._last_app and self._last_app == current_app:
            elapsed = now - self._last_check
            self.app_usage[current_app] = self.app_usage.get(current_app, 0) + elapsed

        self._last_app = current_app
        self._last_check = now

    def get_summary(self):
        """Get a summary of app usage during this session."""
        if not self.app_usage:
            return "No app usage data recorded yet."

        sorted_apps = sorted(self.app_usage.items(), key=lambda x: x[1], reverse=True)
        lines = []
        for app, seconds in sorted_apps[:5]:
            minutes = seconds / 60
            lines.append(f"{app}: {minutes:.0f} min")

        session_duration = (time.time() - self.session_start) / 60
        summary = f"Session: {session_duration:.0f} min. Top apps: " + ", ".join(lines)
        return summary

    def save(self):
        """Save the session log to disk."""
        os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
        log_entry = {
            "session_start": self.session_start,
            "session_end": time.time(),
            "app_usage": self.app_usage,
        }

        logs = []
        if os.path.exists(TRACKER_FILE):
            try:
                with open(TRACKER_FILE, "r") as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []

        logs.append(log_entry)
        with open(TRACKER_FILE, "w") as f:
            json.dump(logs, f, indent=2)
