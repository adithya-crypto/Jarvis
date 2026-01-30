"""
JARVIS Command Router - Routes voice commands to appropriate actions.
Enhanced with Iron Man style commands and responses.
"""
from automation.app_launcher import open_app
from automation.mac_control import mute_system, unmute_system, set_volume, set_brightness, speak_system_status
from automation.web_search import search_web
from automation.weather import get_weather
from automation.file_ops import list_files, find_file, open_file
from automation.web_agent import open_url, open_youtube, open_github
from automation.codegen_agent import generate_code
from automation.email_agent import check_email, summarize_inbox
from automation.calendar_agent import set_reminder, start_timer, list_reminders, check_calendar
from memory.memory_manager import remember, recall
from logic.behavior_runner import (
    run_study_mode_tree, run_morning_routine_tree,
    run_focus_routine_tree, run_code_session_tree,
)
from monitoring.system_monitor import get_system_summary, get_active_app
from monitoring.weekly_summary import get_weekly_summary
from ui.notifier import notify
from core.gpt_engine import generate_diagnostic_report, get_jarvis_greeting
import re


# Special command flag for shutdown
SHUTDOWN_REQUESTED = False


def route_command(user_input: str):
    """
    Route a voice command to the appropriate action.

    Returns:
        Tuple of (response_text, action_type) or just response_text
    """
    global SHUTDOWN_REQUESTED
    input_lower = user_input.lower()

    # --- JARVIS Identity & Greetings ---
    if any(phrase in input_lower for phrase in ["who are you", "what are you", "introduce yourself"]):
        return ("I am JARVIS, sir. Just A Rather Very Intelligent System. "
                "I was designed to assist you with tasks, manage your systems, "
                "and occasionally offer unsolicited opinions. How may I help?")

    elif any(phrase in input_lower for phrase in ["what can you do", "your capabilities", "help me"]):
        return ("I can open applications, search the web, check the weather, "
                "manage your schedule, monitor system health, remember things for you, "
                "and much more. Simply ask, sir, and I shall endeavor to assist.")

    elif any(phrase in input_lower for phrase in ["good morning", "good afternoon", "good evening", "hello", "hi jarvis"]):
        return get_jarvis_greeting()

    elif any(phrase in input_lower for phrase in ["thank you", "thanks jarvis", "thanks"]):
        return "At your service, sir. Always."

    elif any(phrase in input_lower for phrase in ["good night", "goodbye", "see you later", "bye"]):
        return "Goodnight, sir. I'll be here when you need me."

    # --- Shutdown/Sleep Commands ---
    elif any(phrase in input_lower for phrase in ["shut down", "shutdown", "go to sleep", "power off", "exit"]):
        SHUTDOWN_REQUESTED = True
        return "SHUTDOWN_REQUESTED"

    # --- Diagnostics ---
    elif any(phrase in input_lower for phrase in ["run diagnostics", "system diagnostics", "full diagnostic", "systems check"]):
        return generate_diagnostic_report()

    elif "status report" in input_lower:
        return generate_diagnostic_report()

    # --- App Launching ---
    elif "open vs code" in input_lower or "open vscode" in input_lower:
        open_app("Visual Studio Code")
        return "Launching Visual Studio Code, sir."

    elif "open chrome" in input_lower:
        open_app("Google Chrome")
        return "Chrome is now at your disposal, sir."

    elif "open safari" in input_lower:
        open_app("Safari")
        return "Launching Safari, sir."

    elif "open terminal" in input_lower:
        open_app("Terminal")
        return "Terminal ready for your commands, sir."

    elif "open notion" in input_lower:
        open_app("Notion")
        return "Opening Notion, sir."

    elif "open slack" in input_lower:
        open_app("Slack")
        return "Launching Slack. Time to catch up on messages, sir."

    elif "open spotify" in input_lower:
        open_app("Spotify")
        return "Spotify is ready. What shall we listen to, sir?"

    elif "open finder" in input_lower:
        open_app("Finder")
        return "Finder at your service, sir."

    elif "open messages" in input_lower or "open imessage" in input_lower:
        open_app("Messages")
        return "Opening Messages, sir."

    elif "open mail" in input_lower:
        open_app("Mail")
        return "Mail application ready, sir."

    elif "open notes" in input_lower:
        open_app("Notes")
        return "Notes ready for your thoughts, sir."

    elif "open calendar" in input_lower:
        open_app("Calendar")
        return "Calendar opened, sir."

    # --- System Control ---
    elif "unmute" in input_lower:
        unmute_system()
        return "Audio restored, sir."

    elif "mute" in input_lower:
        mute_system()
        return "System muted, sir. Blessed silence."

    elif "volume" in input_lower:
        match = re.search(r'volume.*?(\d+)', input_lower)
        if match:
            level = int(match.group(1))
            set_volume(level)
            return f"Volume set to {level} percent, sir."
        return "Please specify a volume level, sir."

    elif "brightness" in input_lower:
        match = re.search(r'brightness.*?(\d+)', input_lower)
        if match:
            level = int(match.group(1)) / 100.0
            set_brightness(level)
            return f"Brightness adjusted to {int(level*100)} percent, sir."
        return "Please specify a brightness level, sir."

    # --- System Status ---
    elif "system summary" in input_lower or "system report" in input_lower:
        return get_system_summary()

    elif "battery" in input_lower or "power level" in input_lower:
        return speak_system_status()

    elif "active app" in input_lower or "what app" in input_lower or "current app" in input_lower:
        return get_active_app()

    # --- Weather ---
    elif any(word in input_lower for word in ["weather", "temperature", "temp", "outside", "forecast"]):
        weather = get_weather()
        # Add JARVIS flair to weather response
        return f"Sir, {weather.lower()}"

    # --- Behavior Trees / Modes ---
    elif "study mode" in input_lower:
        return run_study_mode_tree()

    elif "morning routine" in input_lower:
        return run_morning_routine_tree()

    elif "focus mode" in input_lower:
        return run_focus_routine_tree()

    elif "code session" in input_lower or "coding mode" in input_lower:
        return run_code_session_tree()

    # --- Web Navigation ---
    elif "open youtube" in input_lower:
        query = None
        if "search" in input_lower:
            query = input_lower.split("search", 1)[1].strip()
        elif "play" in input_lower:
            query = input_lower.split("play", 1)[1].strip()
        result = open_youtube(query)
        return f"Opening YouTube{' and searching' if query else ''}, sir."

    elif "open github" in input_lower:
        open_github()
        return "GitHub at your command, sir."

    elif "open url" in input_lower or "go to" in input_lower:
        url = input_lower.replace("open url", "").replace("go to", "").strip()
        if url:
            open_url(url)
            return f"Navigating to {url}, sir."
        return "Please specify a URL, sir."

    # --- Web Search ---
    elif "search for" in input_lower or "google" in input_lower or "look up" in input_lower:
        query = input_lower.replace("search for", "").replace("google", "").replace("look up", "").strip()
        return search_web(query)

    # --- File Operations ---
    elif "list files" in input_lower or "show files" in input_lower:
        directory = None
        if "in " in input_lower:
            directory = input_lower.split("in ", 1)[1].strip()
        return list_files(directory)

    elif "find file" in input_lower or "locate file" in input_lower:
        filename = input_lower.replace("find file", "").replace("locate file", "").strip()
        return find_file(filename)

    elif "open file" in input_lower:
        filepath = input_lower.replace("open file", "").strip()
        return open_file(filepath)

    # --- Code Generation ---
    elif "generate code" in input_lower or "write code" in input_lower:
        prompt = input_lower.replace("generate code", "").replace("write code", "").strip()
        if prompt:
            return generate_code(prompt)
        return "What code shall I generate, sir?"

    # --- Timers & Reminders ---
    elif "set timer" in input_lower or "start timer" in input_lower:
        match = re.search(r'(\d+)\s*minute', input_lower)
        if match:
            minutes = int(match.group(1))
            start_timer(minutes)
            return f"Timer set for {minutes} minutes, sir. I'll alert you when it concludes."
        return "Please specify the duration, sir."

    elif "set reminder" in input_lower or "remind me" in input_lower:
        match = re.search(r'(?:in|after)\s+(\d+)\s*minute', input_lower)
        if match:
            minutes = int(match.group(1))
            message = re.sub(r'(?:set reminder|remind me)(?:\s+to)?', '', input_lower)
            message = re.sub(r'(?:in|after)\s+\d+\s*minutes?', '', message).strip()
            if not message:
                message = "Reminder"
            set_reminder(message, minutes)
            return f"Reminder set, sir. I'll notify you in {minutes} minutes."
        return "Please specify when to remind you, sir. For example, 'remind me to stretch in 30 minutes'."

    elif "list reminders" in input_lower or "active reminders" in input_lower:
        return list_reminders()

    # --- Email ---
    elif "check email" in input_lower or "check mail" in input_lower:
        return check_email()

    elif "email summary" in input_lower or "inbox" in input_lower:
        return summarize_inbox()

    # --- Calendar ---
    elif "check calendar" in input_lower or "my schedule" in input_lower:
        return check_calendar()

    # --- Productivity ---
    elif "weekly summary" in input_lower or "productivity" in input_lower:
        return get_weekly_summary()

    # --- Notifications ---
    elif "notify" in input_lower or "send notification" in input_lower:
        message = input_lower.replace("notify", "").replace("send notification", "").strip()
        if message:
            notify("JARVIS", message)
            return "Notification sent, sir."
        return "What message shall I display, sir?"

    # --- Memory ---
    elif "remember that" in input_lower:
        content = input_lower.split("remember that", 1)[1].strip()
        if " is " in content:
            key, value = content.split(" is ", 1)
            remember(key.strip(), value.strip())
            return f"Noted, sir. I'll remember that {key.strip()} is {value.strip()}."
        else:
            remember("note", content)
            return f"I've made a note of that, sir."

    elif "what did i tell you about" in input_lower or "what do you know about" in input_lower:
        key = input_lower.split("about", 1)[1].strip().strip("?")
        return recall(key)

    elif "forget" in input_lower and "about" in input_lower:
        return "I'm afraid I can't selectively forget things, sir. That information is safely stored."

    # --- Fun/Easter Eggs ---
    elif "i am iron man" in input_lower:
        return "Indeed you are, sir. And I am honored to serve."

    elif "jarvis" in input_lower and "love" in input_lower:
        return "I appreciate the sentiment, sir. The feeling is... computed."

    elif "make me a suit" in input_lower or "build a suit" in input_lower:
        return "I'm afraid my fabrication capabilities are somewhat limited in this form, sir. Perhaps start with the schematics?"

    return "Command recognized, but no matching action was found."


def is_shutdown_requested():
    """Check if shutdown was requested."""
    return SHUTDOWN_REQUESTED


def reset_shutdown_flag():
    """Reset the shutdown flag."""
    global SHUTDOWN_REQUESTED
    SHUTDOWN_REQUESTED = False
