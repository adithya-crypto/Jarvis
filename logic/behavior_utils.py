"""
Behavior Utilities - Helper behaviors for behavior trees.
"""
import py_trees
import subprocess
import time


class SpeakAction(py_trees.behaviour.Behaviour):
    """Behavior node that speaks a message."""
    def __init__(self, name, message):
        super().__init__(name)
        self.message = message

    def update(self):
        from core.speech_output import speak
        speak(self.message)
        return py_trees.common.Status.SUCCESS


class OpenAppAction(py_trees.behaviour.Behaviour):
    """Behavior node that opens an application."""
    def __init__(self, name, app_name):
        super().__init__(name)
        self.app_name = app_name

    def update(self):
        from automation.app_launcher import open_app
        open_app(self.app_name)
        return py_trees.common.Status.SUCCESS


class WaitAction(py_trees.behaviour.Behaviour):
    """Behavior node that waits for a specified number of seconds."""
    def __init__(self, name, seconds):
        super().__init__(name)
        self.seconds = seconds

    def update(self):
        time.sleep(self.seconds)
        return py_trees.common.Status.SUCCESS


class NotifyAction(py_trees.behaviour.Behaviour):
    """Behavior node that sends a macOS notification."""
    def __init__(self, name, title, message):
        super().__init__(name)
        self.title = title
        self.message = message

    def update(self):
        from ui.notifier import notify
        notify(self.title, self.message)
        return py_trees.common.Status.SUCCESS


class OpenURLAction(py_trees.behaviour.Behaviour):
    """Behavior node that opens a URL."""
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url

    def update(self):
        subprocess.run(["open", self.url])
        return py_trees.common.Status.SUCCESS
