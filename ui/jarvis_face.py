"""
JARVIS Face - Cinematic Iron Man style boot sequence and status displays.
"""
import time
import sys
import psutil
from datetime import datetime

# ANSI color codes for terminal styling
class Colors:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def _print_slow(text, delay=0.02, end='\n'):
    """Print text character by character for cinematic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def _print_status(label, status="OK", delay=0.3):
    """Print a system check line with status."""
    dots = "." * (35 - len(label))
    if status == "OK":
        status_color = Colors.GREEN
    elif status == "WARN":
        status_color = Colors.YELLOW
    else:
        status_color = Colors.RED

    sys.stdout.write(f"  {Colors.CYAN}{label}{Colors.DIM}{dots}{Colors.RESET}")
    sys.stdout.flush()
    time.sleep(delay)
    print(f"[{status_color}{status}{Colors.RESET}]")


def _get_time_greeting():
    """Get appropriate greeting based on time of day."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning, sir.", "I trust you slept well."
    elif 12 <= hour < 17:
        return "Good afternoon, sir.", "Ready to assist."
    elif 17 <= hour < 21:
        return "Good evening, sir.", "How may I be of service?"
    else:
        return "Working late again, sir?", "I'll keep the systems warm."


def show_jarvis_boot(speak_callback=None):
    """Display cinematic JARVIS boot-up sequence with system checks."""

    # Clear screen
    print("\033[2J\033[H", end="")

    # Arc Reactor initialization
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("                    ████████████                    ")
    print("                ████            ████                ")
    print("              ██      ████████      ██              ")
    print("            ██    ████        ████    ██            ")
    print("           ██   ██    ██████    ██   ██            ")
    print("          ██   ██   ██      ██   ██   ██           ")
    print("          ██  ██   ██   ██   ██   ██  ██           ")
    print("          ██  ██   ██   ██   ██   ██  ██           ")
    print("          ██   ██   ██      ██   ██   ██           ")
    print("           ██   ██    ██████    ██   ██            ")
    print("            ██    ████        ████    ██            ")
    print("              ██      ████████      ██              ")
    print("                ████            ████                ")
    print("                    ████████████                    ")
    print(f"{Colors.RESET}")

    time.sleep(0.5)

    # JARVIS Title
    print(f"{Colors.CYAN}{Colors.BOLD}")
    _print_slow("         ╔═══════════════════════════════════════════════╗", delay=0.005)
    _print_slow("         ║                                               ║", delay=0.005)
    _print_slow("         ║        J.A.R.V.I.S.  INTERFACE  v3.0          ║", delay=0.005)
    _print_slow("         ║   Just A Rather Very Intelligent System       ║", delay=0.005)
    _print_slow("         ║                                               ║", delay=0.005)
    _print_slow("         ╚═══════════════════════════════════════════════╝", delay=0.005)
    print(f"{Colors.RESET}")

    time.sleep(0.3)

    # System initialization
    print(f"\n{Colors.WHITE}  Initializing Stark Industries OS...{Colors.RESET}\n")
    time.sleep(0.3)

    # Core Systems Check
    print(f"  {Colors.YELLOW}[CORE SYSTEMS]{Colors.RESET}")
    _print_status("Arc Reactor Power Link", "OK")
    _print_status("Neural Network Interface", "OK")
    _print_status("Voice Recognition Module", "OK")
    _print_status("Speech Synthesis Engine", "OK")

    print(f"\n  {Colors.YELLOW}[AI ENGINE]{Colors.RESET}")
    _print_status("Gemini 2.0 Flash Neural Core", "OK")
    _print_status("Context Memory Banks", "OK")
    _print_status("Personality Matrix", "OK")

    print(f"\n  {Colors.YELLOW}[SYSTEM DIAGNOSTICS]{Colors.RESET}")

    # Real system checks
    battery = psutil.sensors_battery()
    if battery:
        bat_status = "OK" if battery.percent > 20 else ("WARN" if battery.percent > 10 else "FAIL")
        _print_status(f"Power Reserve ({battery.percent}%)", bat_status)
    else:
        _print_status("Power Reserve (AC)", "OK")

    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_status = "OK" if cpu_percent < 80 else "WARN"
    _print_status(f"Processor Load ({cpu_percent:.0f}%)", cpu_status)

    mem = psutil.virtual_memory()
    mem_status = "OK" if mem.percent < 85 else "WARN"
    _print_status(f"Memory Allocation ({mem.percent:.0f}%)", mem_status)

    disk = psutil.disk_usage('/')
    disk_status = "OK" if disk.percent < 90 else "WARN"
    _print_status(f"Storage Capacity ({disk.percent:.0f}%)", disk_status)

    print(f"\n  {Colors.YELLOW}[SECURITY]{Colors.RESET}")
    _print_status("Firewall Protocols", "OK")
    _print_status("Encryption Layer", "OK")

    time.sleep(0.5)

    # Final status
    print(f"\n  {Colors.GREEN}{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.GREEN}{Colors.BOLD}  ALL SYSTEMS OPERATIONAL - JARVIS ONLINE{Colors.RESET}")
    print(f"  {Colors.GREEN}{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    # Time-aware greeting
    greeting, subtext = _get_time_greeting()
    print(f"\n  {Colors.CYAN}{greeting}{Colors.RESET}")
    print(f"  {Colors.DIM}{subtext}{Colors.RESET}")

    timestamp = datetime.now().strftime("%A, %B %d, %Y - %H:%M")
    print(f"\n  {Colors.DIM}Session started: {timestamp}{Colors.RESET}")
    print(f"  {Colors.DIM}Awaiting voice command or wake word 'Jarvis'...{Colors.RESET}\n")

    # Speak the greeting if callback provided
    if speak_callback:
        speak_callback(f"{greeting} {subtext} All systems are operational.")

    return greeting


def show_listening():
    """Display a listening indicator."""
    print(f"  {Colors.CYAN}[{Colors.BOLD}*{Colors.RESET}{Colors.CYAN}] Listening...{Colors.RESET}")


def show_thinking():
    """Display a thinking indicator."""
    print(f"  {Colors.YELLOW}[{Colors.BOLD}~{Colors.RESET}{Colors.YELLOW}] Processing request...{Colors.RESET}")


def show_speaking():
    """Display a speaking indicator."""
    print(f"  {Colors.GREEN}[{Colors.BOLD}>{Colors.RESET}{Colors.GREEN}] Speaking...{Colors.RESET}")


def show_wake_word_detected():
    """Display wake word detection."""
    print(f"\n  {Colors.CYAN}{Colors.BOLD}[JARVIS ACTIVATED]{Colors.RESET}")


def show_command(command):
    """Display the recognized command."""
    print(f"  {Colors.WHITE}Command: \"{command}\"{Colors.RESET}")


def show_response(response):
    """Display JARVIS response."""
    # Truncate if too long for display
    display_response = response[:100] + "..." if len(response) > 100 else response
    print(f"  {Colors.GREEN}JARVIS: {display_response}{Colors.RESET}\n")


def show_error(message):
    """Display an error message."""
    print(f"  {Colors.RED}[ERROR] {message}{Colors.RESET}")


def show_warning(message):
    """Display a warning message."""
    print(f"  {Colors.YELLOW}[WARNING] {message}{Colors.RESET}")


def show_shutdown():
    """Display shutdown sequence."""
    print(f"\n  {Colors.YELLOW}[SHUTDOWN SEQUENCE INITIATED]{Colors.RESET}")
    _print_status("Saving session data", "OK", delay=0.2)
    _print_status("Closing neural connections", "OK", delay=0.2)
    _print_status("Powering down subsystems", "OK", delay=0.2)
    print(f"\n  {Colors.CYAN}Goodbye, sir. It's been a pleasure.{Colors.RESET}")
    print(f"  {Colors.DIM}JARVIS entering standby mode...{Colors.RESET}\n")
