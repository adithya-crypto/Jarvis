"""
JARVIS Proactive Monitor - Background daemon that monitors system health
and proactively alerts the user when something needs attention.
"""
import threading
import time
import psutil
from datetime import datetime, timedelta


class JarvisMonitor:
    """
    Background monitor that runs periodic system checks and triggers
    alerts via a speech callback when something needs attention.
    """

    def __init__(self, speak_callback=None):
        """
        Initialize the monitor.

        Args:
            speak_callback: Function to call when JARVIS needs to speak an alert.
                           Should accept a single string argument.
        """
        self.speak_callback = speak_callback
        self._running = False
        self._thread = None
        self._last_alerts = {}  # Track when alerts were last triggered
        self._alert_cooldown = 300  # 5 minutes between repeat alerts
        self._session_start = datetime.now()
        self._is_speaking = False  # Flag to prevent interruption
        self._is_listening = False

        # Alert thresholds
        self.battery_warning = 20
        self.battery_critical = 10
        self.cpu_warning = 90
        self.memory_warning = 90
        self.disk_warning = 95
        self.work_session_reminder = 120  # 2 hours in minutes

    def set_speaking(self, is_speaking):
        """Set flag indicating JARVIS is currently speaking."""
        self._is_speaking = is_speaking

    def set_listening(self, is_listening):
        """Set flag indicating JARVIS is currently listening."""
        self._is_listening = is_listening

    def _can_alert(self, alert_type):
        """Check if enough time has passed to trigger this alert again."""
        if alert_type not in self._last_alerts:
            return True
        elapsed = (datetime.now() - self._last_alerts[alert_type]).total_seconds()
        return elapsed >= self._alert_cooldown

    def _trigger_alert(self, alert_type, message):
        """Trigger an alert if conditions are met."""
        if not self._can_alert(alert_type):
            return

        # Don't interrupt if JARVIS is speaking or listening
        if self._is_speaking or self._is_listening:
            return

        self._last_alerts[alert_type] = datetime.now()

        if self.speak_callback:
            print(f"\n  [JARVIS ALERT] {message}")
            self.speak_callback(message)

    def _check_battery(self):
        """Check battery status and alert if needed."""
        battery = psutil.sensors_battery()
        if not battery or battery.power_plugged:
            return

        if battery.percent <= self.battery_critical:
            self._trigger_alert(
                "battery_critical",
                f"Sir, power reserves are critically low at {battery.percent} percent. "
                "I strongly recommend connecting to a power source immediately."
            )
        elif battery.percent <= self.battery_warning:
            self._trigger_alert(
                "battery_warning",
                f"Sir, power reserves are at {battery.percent} percent. "
                "You may want to find a charging station soon."
            )

    def _check_cpu(self):
        """Check CPU usage and alert if consistently high."""
        cpu = psutil.cpu_percent(interval=2)
        if cpu >= self.cpu_warning:
            self._trigger_alert(
                "cpu_warning",
                f"Sir, the processor is running quite hot at {cpu:.0f} percent. "
                "Perhaps close some resource-intensive applications?"
            )

    def _check_memory(self):
        """Check memory usage and alert if high."""
        mem = psutil.virtual_memory()
        if mem.percent >= self.memory_warning:
            self._trigger_alert(
                "memory_warning",
                f"Sir, memory utilization is at {mem.percent:.0f} percent. "
                "The system may become sluggish."
            )

    def _check_disk(self):
        """Check disk usage and alert if nearly full."""
        disk = psutil.disk_usage('/')
        if disk.percent >= self.disk_warning:
            self._trigger_alert(
                "disk_warning",
                f"Sir, storage capacity is nearly depleted at {disk.percent:.0f} percent. "
                "Consider archiving some files."
            )

    def _check_work_session(self):
        """Remind user to take breaks during long sessions."""
        session_minutes = (datetime.now() - self._session_start).total_seconds() / 60

        # Remind every 2 hours
        if session_minutes >= self.work_session_reminder:
            reminder_count = int(session_minutes // self.work_session_reminder)
            alert_key = f"work_session_{reminder_count}"

            if self._can_alert(alert_key):
                hours = session_minutes / 60
                self._trigger_alert(
                    alert_key,
                    f"Sir, you've been working for {hours:.1f} hours. "
                    "Perhaps a short break would be beneficial?"
                )

    def _check_late_night(self):
        """Remind user if working very late."""
        hour = datetime.now().hour
        if 23 <= hour or hour < 5:
            self._trigger_alert(
                "late_night",
                "Sir, it's getting quite late. "
                "Your productivity may suffer without proper rest."
            )

    def _monitor_loop(self):
        """Main monitoring loop that runs in background thread."""
        check_interval = 60  # Check every 60 seconds

        while self._running:
            try:
                self._check_battery()
                self._check_cpu()
                self._check_memory()
                self._check_disk()
                self._check_work_session()
                self._check_late_night()
            except Exception as e:
                print(f"  [Monitor Error] {e}")

            # Sleep in small increments to allow quick shutdown
            for _ in range(check_interval):
                if not self._running:
                    break
                time.sleep(1)

    def start(self):
        """Start the background monitor."""
        if self._running:
            return

        self._running = True
        self._session_start = datetime.now()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        print("  [Monitor] Background monitoring active.")

    def stop(self):
        """Stop the background monitor."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("  [Monitor] Background monitoring stopped.")

    def get_session_duration(self):
        """Get the current session duration in minutes."""
        return (datetime.now() - self._session_start).total_seconds() / 60

    def get_status(self):
        """Get the current monitor status."""
        return {
            "running": self._running,
            "session_minutes": self.get_session_duration(),
            "alerts_triggered": len(self._last_alerts),
        }


# Global monitor instance
_monitor_instance = None


def get_monitor():
    """Get or create the global monitor instance."""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = JarvisMonitor()
    return _monitor_instance


def start_monitoring(speak_callback=None):
    """Start the global monitor with the given speech callback."""
    monitor = get_monitor()
    monitor.speak_callback = speak_callback
    monitor.start()
    return monitor


def stop_monitoring():
    """Stop the global monitor."""
    monitor = get_monitor()
    monitor.stop()
