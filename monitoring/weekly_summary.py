"""
Weekly Summary - Generates a summary from productivity logs.
"""
import json
import os
import time

TRACKER_FILE = "data/productivity_log.json"


def get_weekly_summary():
    """Generate a summary of the past week's productivity data."""
    if not os.path.exists(TRACKER_FILE):
        return "No productivity data available yet. Start a session first."

    try:
        with open(TRACKER_FILE, "r") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return "No productivity data available yet."

    if not logs:
        return "No productivity data available yet."

    # Filter to last 7 days
    one_week_ago = time.time() - (7 * 24 * 3600)
    recent = [log for log in logs if log.get("session_start", 0) > one_week_ago]

    if not recent:
        return "No sessions recorded in the past week."

    total_time = sum(
        (log.get("session_end", 0) - log.get("session_start", 0))
        for log in recent
    )

    # Aggregate app usage across sessions
    app_totals = {}
    for log in recent:
        for app, seconds in log.get("app_usage", {}).items():
            app_totals[app] = app_totals.get(app, 0) + seconds

    top_apps = sorted(app_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    app_lines = ", ".join(f"{app}: {secs/60:.0f} min" for app, secs in top_apps)

    total_hours = total_time / 3600
    return (
        f"Weekly summary: {len(recent)} sessions, {total_hours:.1f} hours total. "
        f"Top apps: {app_lines}."
    )
