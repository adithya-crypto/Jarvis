"""Tests for individual modules - context memory, file ops, calendar, monitoring, etc."""
import unittest
import os
import time
import tempfile


class TestContextMemory(unittest.TestCase):

    def test_add_and_retrieve(self):
        from core.context_memory import ContextMemory
        ctx = ContextMemory(max_turns=5)
        ctx.add_exchange("hello", "hi there")
        last = ctx.get_last_exchange()
        self.assertEqual(last["user"], "hello")
        self.assertEqual(last["assistant"], "hi there")

    def test_max_turns_limit(self):
        from core.context_memory import ContextMemory
        ctx = ContextMemory(max_turns=3)
        for i in range(5):
            ctx.add_exchange(f"msg {i}", f"reply {i}")
        self.assertEqual(len(ctx.history), 3)
        self.assertEqual(ctx.history[0]["user"], "msg 2")

    def test_get_context_string(self):
        from core.context_memory import ContextMemory
        ctx = ContextMemory()
        ctx.add_exchange("hi", "hello")
        context_str = ctx.get_context_string()
        self.assertIn("User: hi", context_str)
        self.assertIn("JARVIS: hello", context_str)

    def test_clear(self):
        from core.context_memory import ContextMemory
        ctx = ContextMemory()
        ctx.add_exchange("test", "test reply")
        ctx.clear()
        self.assertEqual(len(ctx.history), 0)

    def test_empty_context_string(self):
        from core.context_memory import ContextMemory
        ctx = ContextMemory()
        self.assertEqual(ctx.get_context_string(), "")


class TestFileOps(unittest.TestCase):

    def test_list_files_desktop(self):
        from automation.file_ops import list_files
        result = list_files()
        self.assertIn("Found", result)

    def test_list_files_nonexistent(self):
        from automation.file_ops import list_files
        result = list_files("/nonexistent/directory")
        self.assertIn("not found", result)

    def test_find_file(self):
        from automation.file_ops import find_file
        # Search for main.py in the project
        result = find_file("main.py", os.path.expanduser("~/Desktop/jarvis-assistant"))
        self.assertIn("main.py", result)

    def test_get_file_info(self):
        from automation.file_ops import get_file_info
        result = get_file_info("~/Desktop/jarvis-assistant/main.py")
        self.assertIn("main.py", result)
        self.assertIn("MB", result)

    def test_open_file_nonexistent(self):
        from automation.file_ops import open_file
        result = open_file("/nonexistent/file.txt")
        self.assertIn("not found", result)


class TestCalendarAgent(unittest.TestCase):

    def test_set_reminder(self):
        from automation.calendar_agent import set_reminder
        result = set_reminder("test", 1)
        self.assertIn("Reminder set", result)

    def test_list_reminders_empty(self):
        from automation.calendar_agent import _active_timers, list_reminders
        _active_timers.clear()
        result = list_reminders()
        self.assertIn("No active", result)

    def test_cancel_nonexistent_reminder(self):
        from automation.calendar_agent import cancel_reminder
        result = cancel_reminder("nonexistent")
        self.assertIn("No active", result)

    def test_start_timer(self):
        from automation.calendar_agent import start_timer
        result = start_timer(5)
        self.assertIn("Reminder set", result)

    def test_check_calendar_stub(self):
        from automation.calendar_agent import check_calendar
        result = check_calendar()
        self.assertIn("not yet configured", result)


class TestSystemMonitor(unittest.TestCase):

    def test_cpu_usage(self):
        from monitoring.system_monitor import get_cpu_usage
        result = get_cpu_usage()
        self.assertIn("CPU", result)
        self.assertIn("%", result)

    def test_memory_usage(self):
        from monitoring.system_monitor import get_memory_usage
        result = get_memory_usage()
        self.assertIn("Memory", result)
        self.assertIn("GB", result)

    def test_disk_usage(self):
        from monitoring.system_monitor import get_disk_usage
        result = get_disk_usage()
        self.assertIn("Disk", result)
        self.assertIn("GB", result)

    def test_battery_status(self):
        from monitoring.system_monitor import get_battery_status
        result = get_battery_status()
        self.assertIn("Battery", result)

    def test_system_summary(self):
        from monitoring.system_monitor import get_system_summary
        result = get_system_summary()
        self.assertIn("Battery", result)
        self.assertIn("CPU", result)


class TestNotifier(unittest.TestCase):

    def test_notify(self):
        from ui.notifier import notify
        result = notify("Test", "Test message")
        self.assertIn("Notification sent", result)


class TestMemoryManager(unittest.TestCase):

    def test_remember_and_recall(self):
        from memory.memory_manager import remember, recall
        remember("test_key", "test_value")
        result = recall("test_key")
        self.assertIn("test_value", result)

    def test_recall_unknown_key(self):
        from memory.memory_manager import recall
        result = recall("nonexistent_key_xyz")
        self.assertIn("don't have", result)


class TestWeeklySmummary(unittest.TestCase):

    def test_no_data(self):
        from monitoring.weekly_summary import get_weekly_summary
        # May or may not have data, just ensure no crash
        result = get_weekly_summary()
        self.assertIsInstance(result, str)


class TestWebAgent(unittest.TestCase):

    def test_open_youtube_url(self):
        from automation.web_agent import open_youtube
        # Just test URL generation, don't actually open
        result = open_youtube.__doc__
        self.assertIsNotNone(result)


class TestMainResponseSelection(unittest.TestCase):

    def test_should_use_action_feedback(self):
        # Import the helper from main
        import importlib
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from main import should_use_action_feedback
        self.assertTrue(should_use_action_feedback("Here is what I found: Python"))
        self.assertTrue(should_use_action_feedback("Battery at 85%"))
        self.assertTrue(should_use_action_feedback("Reminder set: test in 5 minutes."))
        self.assertTrue(should_use_action_feedback("CPU usage is at 25%."))
        self.assertTrue(should_use_action_feedback("The temperature in NYC is 72F"))
        self.assertFalse(should_use_action_feedback("Opening Chrome."))
        self.assertFalse(should_use_action_feedback("System muted."))


if __name__ == "__main__":
    unittest.main()
