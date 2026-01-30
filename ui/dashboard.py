"""
Dashboard - Iron Man style terminal status display for JARVIS.
"""
import psutil
from datetime import datetime
from ui.jarvis_face import Colors


class JarvisDashboard:
    """Real-time JARVIS status dashboard."""

    def __init__(self):
        self.commands_processed = 0
        self.last_command = None
        self.last_response = None
        self.session_start = datetime.now()
        self.current_mode = "Normal"

    def _progress_bar(self, percent, width=20, fill_char="█", empty_char="░"):
        """Generate a progress bar string."""
        filled = int(width * percent / 100)
        empty = width - filled
        return f"{fill_char * filled}{empty_char * empty}"

    def _colorize_percent(self, percent, reverse=False):
        """Get color based on percentage (green=low, red=high or reversed)."""
        if reverse:
            if percent >= 50:
                return Colors.GREEN
            elif percent >= 20:
                return Colors.YELLOW
            else:
                return Colors.RED
        else:
            if percent < 60:
                return Colors.GREEN
            elif percent < 85:
                return Colors.YELLOW
            else:
                return Colors.RED

    def log_command(self, command, response):
        """Log a processed command."""
        self.commands_processed += 1
        self.last_command = command
        self.last_response = response[:80] if response else None

    def set_mode(self, mode):
        """Set the current operating mode."""
        self.current_mode = mode

    def get_uptime(self):
        """Get session uptime as formatted string."""
        delta = datetime.now() - self.session_start
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def render(self):
        """Render the full dashboard to terminal."""
        # Get system stats
        battery = psutil.sensors_battery()
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Clear line and print header
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}           J.A.R.V.I.S. REAL-TIME STATUS{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")

        # Session info
        print(f"\n  {Colors.WHITE}Session Uptime:{Colors.RESET}    {Colors.GREEN}{self.get_uptime()}{Colors.RESET}")
        print(f"  {Colors.WHITE}Commands Processed:{Colors.RESET} {Colors.GREEN}{self.commands_processed}{Colors.RESET}")
        print(f"  {Colors.WHITE}Operating Mode:{Colors.RESET}     {Colors.CYAN}{self.current_mode}{Colors.RESET}")

        print(f"\n{Colors.YELLOW}  ─── SYSTEM VITALS ───{Colors.RESET}")

        # Battery
        if battery:
            bat_color = self._colorize_percent(battery.percent, reverse=True)
            bat_bar = self._progress_bar(battery.percent)
            status = "⚡ Charging" if battery.power_plugged else "🔋 Battery"
            print(f"  {Colors.WHITE}Power:  {Colors.RESET}{bat_color}{bat_bar}{Colors.RESET} {battery.percent:3.0f}% {Colors.DIM}{status}{Colors.RESET}")
        else:
            print(f"  {Colors.WHITE}Power:  {Colors.GREEN}AC Connected{Colors.RESET}")

        # CPU
        cpu_color = self._colorize_percent(cpu_percent)
        cpu_bar = self._progress_bar(cpu_percent)
        print(f"  {Colors.WHITE}CPU:    {Colors.RESET}{cpu_color}{cpu_bar}{Colors.RESET} {cpu_percent:3.0f}%")

        # Memory
        mem_color = self._colorize_percent(mem.percent)
        mem_bar = self._progress_bar(mem.percent)
        mem_used = mem.used / (1024**3)
        mem_total = mem.total / (1024**3)
        print(f"  {Colors.WHITE}Memory: {Colors.RESET}{mem_color}{mem_bar}{Colors.RESET} {mem.percent:3.0f}% {Colors.DIM}({mem_used:.1f}/{mem_total:.1f} GB){Colors.RESET}")

        # Disk
        disk_color = self._colorize_percent(disk.percent)
        disk_bar = self._progress_bar(disk.percent)
        print(f"  {Colors.WHITE}Disk:   {Colors.RESET}{disk_color}{disk_bar}{Colors.RESET} {disk.percent:3.0f}%")

        # Last command
        if self.last_command:
            print(f"\n{Colors.YELLOW}  ─── LAST INTERACTION ───{Colors.RESET}")
            print(f"  {Colors.WHITE}Command:{Colors.RESET}  \"{self.last_command[:45]}{'...' if len(self.last_command) > 45 else ''}\"")
            if self.last_response:
                print(f"  {Colors.WHITE}Response:{Colors.RESET} \"{self.last_response[:45]}{'...' if len(self.last_response) > 45 else ''}\"")

        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"  {Colors.DIM}Say \"Jarvis\" to activate • Ctrl+C to shutdown{Colors.RESET}\n")


def print_dashboard():
    """Print a simple terminal dashboard with system stats."""
    dashboard = JarvisDashboard()
    dashboard.render()


def print_mini_status():
    """Print a compact one-line status."""
    battery = psutil.sensors_battery()
    cpu = psutil.cpu_percent(interval=0.1)

    bat_str = f"🔋{battery.percent}%" if battery else "⚡AC"
    print(f"  {Colors.DIM}[{bat_str} | CPU:{cpu:.0f}%]{Colors.RESET}")
