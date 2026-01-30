"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
Main entry point for the Iron Man style AI assistant.
"""
import sys
import time
import signal

from core.voice_input import listen_to_command
from core.gpt_engine import ask_gpt, get_jarvis_greeting
from core.speech_output import speak, speak_greeting, play_sound
from core.command_router import route_command, is_shutdown_requested, reset_shutdown_flag
from core.context_memory import ContextMemory
from core.wake_word import wait_for_wake_word
from ui.jarvis_face import (
    show_jarvis_boot, show_shutdown, show_wake_word_detected,
    show_command, show_response, show_listening, Colors
)
from ui.dashboard import JarvisDashboard
from monitoring.jarvis_monitor import start_monitoring, stop_monitoring, get_monitor
from monitoring.productivity_tracker import ProductivityTracker


# Global state
_running = True
_context = None
_dashboard = None
_tracker = None


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global _running
    _running = False
    print(f"\n\n  {Colors.YELLOW}[INTERRUPT RECEIVED]{Colors.RESET}")


def should_use_action_feedback(action_feedback):
    """Determine if the action feedback contains meaningful data to speak back."""
    # These responses already have good JARVIS-style content
    data_indicators = [
        "Here is what I found",        # Search results
        "You told me", "I've remembered", "Noted, sir",  # Memory
        "Battery", "Power reserves", "charging",  # Battery/power status
        "System status", "diagnostic",  # System status
        "CPU", "Memory", "Processor", "percent",  # System monitor
        "Disk", "Storage",             # Disk info
        "Timer set", "Reminder set", "alert you",  # Timers
        "Active reminders", "No active",   # Reminder list
        "Code generated",              # Code gen
        "not yet configured",          # Unconfigured features
        "Weekly summary", "sessions",  # Productivity
        "Notification sent",           # Notifications
        "Currently active app",        # Active app
        "I am JARVIS", "designed to assist",  # Identity
        "can open applications",       # Capabilities
        "At your service", "Goodnight",  # Greetings
        "honored to serve", "computed",  # Easter eggs
        "activated", "All systems",    # Mode activation
    ]

    feedback_lower = action_feedback.lower()

    # Weather responses
    if "temperature" in feedback_lower or "weather" in feedback_lower:
        return True

    # File search results
    if "found" in feedback_lower and ("items" in feedback_lower or "match" in feedback_lower):
        return True

    # Check indicators
    return any(indicator.lower() in feedback_lower for indicator in data_indicators)


def process_command(command, context):
    """Process a single command and return the response."""
    global _dashboard

    show_command(command)

    # Route the command
    action_feedback = route_command(command)

    # Check for shutdown request
    if action_feedback == "SHUTDOWN_REQUESTED":
        return None  # Signal shutdown

    # Determine response
    if should_use_action_feedback(action_feedback):
        final_reply = action_feedback
    elif "no matching action" in action_feedback:
        # General conversation - use GPT with context
        final_reply = ask_gpt(command, context_history=context.history)
    else:
        # For simple actions, use the router's JARVIS-style response
        final_reply = action_feedback

    # Save to context memory
    context.add_exchange(command, final_reply)

    # Update dashboard
    if _dashboard:
        _dashboard.log_command(command, final_reply)

    return final_reply


def listen_for_followup(timeout=4):
    """
    Listen briefly for a follow-up command without requiring wake word.
    Returns the command if heard, None if silence.
    """
    print(f"  {Colors.DIM}[Listening for follow-up...]{Colors.RESET}")
    try:
        command = listen_to_command(timeout=timeout, phrase_time_limit=8)
        if command and len(command.strip()) > 2:
            return command
    except Exception:
        pass
    return None


def graceful_shutdown(tracker):
    """Perform graceful shutdown sequence."""
    global _running
    _running = False

    print()
    show_shutdown()

    # Save productivity data
    if tracker:
        tracker.save()
        print(f"  {Colors.DIM}Session data saved.{Colors.RESET}")

    # Stop monitoring
    stop_monitoring()

    # Speak goodbye
    speak("Shutting down, sir. It has been a pleasure serving you.")

    time.sleep(1)
    sys.exit(0)


def main():
    """Main JARVIS entry point."""
    global _running, _context, _dashboard, _tracker

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize components
    _context = ContextMemory(max_turns=10)
    _dashboard = JarvisDashboard()
    _tracker = ProductivityTracker()

    # Cinematic boot sequence
    show_jarvis_boot()

    # Start background monitor with speech callback
    monitor = start_monitoring(speak_callback=speak)

    # Speak boot greeting
    greeting = get_jarvis_greeting()
    speak_greeting(greeting)

    print(f"\n  {Colors.DIM}Awaiting wake word 'Jarvis'...{Colors.RESET}\n")

    while _running:
        try:
            # Tick productivity tracker
            _tracker.tick()

            # Wait for wake word
            if wait_for_wake_word():
                # Mark monitor as busy
                monitor.set_listening(True)

                show_wake_word_detected()
                play_sound("pop")

                # Brief pause for mic reset after wake word detection
                time.sleep(0.5)
                speak("Yes sir?")
                # Allow TTS to fully complete and mic to reset before listening
                time.sleep(1.2)

                # Continuous conversation loop
                conversation_active = True
                while conversation_active and _running:
                    show_listening()

                    # Listen for command
                    command = listen_to_command()

                    if command:
                        # Process the command
                        monitor.set_speaking(True)
                        response = process_command(command, _context)
                        monitor.set_speaking(False)

                        # Check for shutdown
                        if response is None:
                            graceful_shutdown(_tracker)

                        # Speak response
                        show_response(response)
                        speak(response)

                        # Allow TTS to fully complete before listening for follow-up
                        time.sleep(1.0)

                        # Check for follow-up (no wake word needed)
                        followup = listen_for_followup(timeout=3)
                        if followup:
                            # Process follow-up
                            monitor.set_speaking(True)
                            response = process_command(followup, _context)
                            monitor.set_speaking(False)

                            if response is None:
                                graceful_shutdown(_tracker)

                            show_response(response)
                            speak(response)
                        else:
                            # No follow-up, exit conversation mode
                            conversation_active = False
                    else:
                        # Didn't hear anything
                        print(f"  {Colors.DIM}[No command detected]{Colors.RESET}")
                        conversation_active = False

                # Resume monitoring
                monitor.set_listening(False)
                print(f"\n  {Colors.DIM}Awaiting wake word 'Jarvis'...{Colors.RESET}\n")

        except KeyboardInterrupt:
            graceful_shutdown(_tracker)
        except Exception as e:
            print(f"  {Colors.RED}[ERROR] {e}{Colors.RESET}")
            time.sleep(1)

    # Clean shutdown
    graceful_shutdown(_tracker)


if __name__ == "__main__":
    main()
