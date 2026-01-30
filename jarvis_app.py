#!/usr/bin/env python3
"""
J.A.R.V.I.S. Application Launcher
Launches either the terminal or GUI version of JARVIS.
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)


def launch_terminal():
    """Launch JARVIS in terminal mode."""
    from main import main
    main()


def launch_gui():
    """Launch JARVIS with graphical interface."""
    import threading
    from ui.jarvis_gui import JarvisGUI
    from core.gpt_engine import get_jarvis_greeting
    from core.speech_output import speak
    from core.command_router import route_command
    from core.context_memory import ContextMemory
    from core.voice_input import listen_to_command
    from core.wake_word import wait_for_wake_word
    from monitoring.jarvis_monitor import start_monitoring, stop_monitoring

    # Initialize
    context = ContextMemory()
    gui = JarvisGUI()

    # Voice processing loop in background
    def voice_loop():
        # Start monitor
        monitor = start_monitoring(speak_callback=speak)

        gui.log_system_message("Voice systems initialized")
        gui.set_status('online')

        while True:
            try:
                gui.set_listening(False)
                gui.set_status('online')

                # Wait for wake word
                if wait_for_wake_word():
                    gui.set_listening(True)
                    gui.set_status('listening')
                    gui.log_system_message("Wake word detected")

                    speak("Yes sir?")

                    # Listen for command
                    command = listen_to_command()

                    if command:
                        gui.log_user_command(command)
                        gui.set_status('processing')

                        # Process command
                        response = route_command(command)

                        if response == "SHUTDOWN_REQUESTED":
                            gui.log_system_message("Shutdown requested")
                            speak("Shutting down, sir.")
                            stop_monitoring()
                            gui.root.quit()
                            break

                        # Handle response
                        if "no matching action" in response:
                            from core.gpt_engine import ask_gpt
                            response = ask_gpt(command, context_history=context.history)

                        context.add_exchange(command, response)
                        gui.log_jarvis_response(response)
                        gui.set_status('speaking')
                        speak(response)

            except Exception as e:
                gui.log_system_message(f"Error: {e}")

    # Start voice loop in background thread
    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    # Run GUI in main thread
    gui.run()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="J.A.R.V.I.S. - Just A Rather Very Intelligent System")
    parser.add_argument('--gui', action='store_true', help='Launch with graphical interface')
    parser.add_argument('--terminal', action='store_true', help='Launch in terminal mode (default)')

    args = parser.parse_args()

    if args.gui:
        print("Launching JARVIS GUI...")
        launch_gui()
    else:
        launch_terminal()


if __name__ == "__main__":
    main()
