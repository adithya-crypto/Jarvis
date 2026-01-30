import py_trees
import time
import subprocess
import psutil
from automation.app_launcher import open_app
from automation.mac_control import mute_system, unmute_system
from logic.behavior_utils import SpeakAction, OpenAppAction, WaitAction, NotifyAction, OpenURLAction

# ---------- Custom Behavior Nodes ----------

class CheckBattery(py_trees.behaviour.Behaviour):
    def update(self):
        battery = psutil.sensors_battery()
        if battery and battery.percent > 40:
            print(f"🔋 Battery OK: {battery.percent}%")
            return py_trees.common.Status.SUCCESS
        else:
            print("⚠️ Battery too low. Please plug in your Mac.")
            return py_trees.common.Status.FAILURE

class MuteNotifications(py_trees.behaviour.Behaviour):
    def update(self):
        mute_system()
        print("🔕 Notifications muted.")
        return py_trees.common.Status.SUCCESS

class UnmuteNotifications(py_trees.behaviour.Behaviour):
    def update(self):
        unmute_system()
        print("🔊 Notifications unmuted.")
        return py_trees.common.Status.SUCCESS

class OpenNotion(py_trees.behaviour.Behaviour):
    def update(self):
        print("🗂️ Opening Notion...")
        open_app("Notion")
        return py_trees.common.Status.SUCCESS

class StartPomodoro(py_trees.behaviour.Behaviour):
    def update(self):
        print("⏱️ Pomodoro timer started: 25 minutes.")
        from automation.calendar_agent import set_reminder
        set_reminder("Pomodoro break time", 25)
        return py_trees.common.Status.SUCCESS

# ---------- Behavior Tree Definitions ----------

def create_study_behavior_tree():
    root = py_trees.composites.Sequence(name="Study Mode", memory=False)
    root.add_children([
        CheckBattery(name="Check Battery"),
        MuteNotifications(name="Mute Notifications"),
        OpenNotion(name="Open Notion"),
        StartPomodoro(name="Start Timer")
    ])
    return root


def create_morning_routine_tree():
    root = py_trees.composites.Sequence(name="Morning Routine", memory=False)
    root.add_children([
        CheckBattery(name="Check Battery"),
        OpenAppAction(name="Open Chrome", app_name="Google Chrome"),
        OpenAppAction(name="Open Notion", app_name="Notion"),
        NotifyAction(name="Morning Greeting", title="JARVIS", message="Good morning, sir. Systems are online."),
    ])
    return root


def create_focus_routine_tree():
    root = py_trees.composites.Sequence(name="Focus Mode", memory=False)
    root.add_children([
        MuteNotifications(name="Mute Notifications"),
        NotifyAction(name="Focus Alert", title="JARVIS", message="Focus mode activated. Distractions silenced."),
        StartPomodoro(name="Start Timer"),
    ])
    return root


def create_code_session_tree():
    root = py_trees.composites.Sequence(name="Code Session", memory=False)
    root.add_children([
        CheckBattery(name="Check Battery"),
        MuteNotifications(name="Mute Notifications"),
        OpenAppAction(name="Open VS Code", app_name="Visual Studio Code"),
        OpenAppAction(name="Open Terminal", app_name="Terminal"),
        NotifyAction(name="Code Ready", title="JARVIS", message="Code session ready. Good luck, sir."),
    ])
    return root


# ---------- Execution Wrappers ----------

def _run_tree(tree_root, label):
    behaviour_tree = py_trees.trees.BehaviourTree(tree_root)
    behaviour_tree.setup(timeout=15)

    print(f"🌳 Running '{label}' behavior tree...")
    max_ticks = 20
    for _ in range(max_ticks):
        behaviour_tree.tick()
        if behaviour_tree.root.status == py_trees.common.Status.SUCCESS:
            break
        if behaviour_tree.root.status == py_trees.common.Status.FAILURE:
            print(f"⚠️ {label} tree failed.")
            return f"{label} could not complete. Check warnings above."
        time.sleep(0.5)

    print(f"✅ {label} Activated.")
    return f"{label} activated. All systems set."


def run_study_mode_tree():
    return _run_tree(create_study_behavior_tree(), "Study Mode")


def run_morning_routine_tree():
    return _run_tree(create_morning_routine_tree(), "Morning Routine")


def run_focus_routine_tree():
    return _run_tree(create_focus_routine_tree(), "Focus Mode")


def run_code_session_tree():
    return _run_tree(create_code_session_tree(), "Code Session")
