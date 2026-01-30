"""
JARVIS Desktop GUI - Iron Man style graphical interface.
Uses Tkinter for cross-platform compatibility.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import time
import psutil
from datetime import datetime


class JarvisGUI:
    """Iron Man style JARVIS desktop interface."""

    # Color scheme (Iron Man / Arc Reactor inspired)
    COLORS = {
        'bg_dark': '#0a0a12',
        'bg_panel': '#12121a',
        'accent_blue': '#00d4ff',
        'accent_cyan': '#00ffff',
        'accent_gold': '#ffd700',
        'text_primary': '#ffffff',
        'text_secondary': '#888899',
        'text_dim': '#555566',
        'success': '#00ff88',
        'warning': '#ffaa00',
        'error': '#ff4444',
        'border': '#1a1a2e',
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("900x700")
        self.root.configure(bg=self.COLORS['bg_dark'])
        self.root.resizable(True, True)

        # Message queue for thread-safe UI updates
        self.message_queue = queue.Queue()

        # State
        self.is_listening = False
        self.is_speaking = False
        self.session_start = datetime.now()
        self.commands_processed = 0

        # Build UI
        self._create_styles()
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Start update loops
        self._start_update_loops()

        # Callbacks for main.py integration
        self.on_command_callback = None
        self.speech_callback = None

    def _create_styles(self):
        """Create custom ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background=self.COLORS['bg_dark'])
        style.configure('Panel.TFrame', background=self.COLORS['bg_panel'])
        style.configure(
            'Header.TLabel',
            background=self.COLORS['bg_dark'],
            foreground=self.COLORS['accent_cyan'],
            font=('Helvetica', 24, 'bold')
        )
        style.configure(
            'Status.TLabel',
            background=self.COLORS['bg_panel'],
            foreground=self.COLORS['text_secondary'],
            font=('Helvetica', 10)
        )

    def _create_header(self):
        """Create the header with JARVIS logo and status."""
        header = tk.Frame(self.root, bg=self.COLORS['bg_dark'], height=80)
        header.pack(fill='x', padx=20, pady=(20, 10))

        # JARVIS title
        title = tk.Label(
            header,
            text="J.A.R.V.I.S.",
            font=('Helvetica', 28, 'bold'),
            fg=self.COLORS['accent_cyan'],
            bg=self.COLORS['bg_dark']
        )
        title.pack(side='left')

        # Subtitle
        subtitle = tk.Label(
            header,
            text="Just A Rather Very Intelligent System",
            font=('Helvetica', 10),
            fg=self.COLORS['text_dim'],
            bg=self.COLORS['bg_dark']
        )
        subtitle.pack(side='left', padx=(15, 0), pady=(12, 0))

        # Status indicator
        self.status_label = tk.Label(
            header,
            text="● ONLINE",
            font=('Helvetica', 12, 'bold'),
            fg=self.COLORS['success'],
            bg=self.COLORS['bg_dark']
        )
        self.status_label.pack(side='right')

    def _create_main_content(self):
        """Create the main content area."""
        main = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        main.pack(fill='both', expand=True, padx=20, pady=10)

        # Left panel - System status
        left_panel = tk.Frame(main, bg=self.COLORS['bg_panel'], width=280)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        self._create_system_panel(left_panel)

        # Right panel - Conversation
        right_panel = tk.Frame(main, bg=self.COLORS['bg_panel'])
        right_panel.pack(side='right', fill='both', expand=True)
        self._create_conversation_panel(right_panel)

    def _create_system_panel(self, parent):
        """Create the system status panel."""
        # Title
        title = tk.Label(
            parent,
            text="SYSTEM STATUS",
            font=('Helvetica', 12, 'bold'),
            fg=self.COLORS['accent_gold'],
            bg=self.COLORS['bg_panel']
        )
        title.pack(pady=(15, 10))

        # Separator
        sep = tk.Frame(parent, bg=self.COLORS['border'], height=1)
        sep.pack(fill='x', padx=15)

        # Session info
        session_frame = tk.Frame(parent, bg=self.COLORS['bg_panel'])
        session_frame.pack(fill='x', padx=15, pady=15)

        tk.Label(
            session_frame, text="Session Uptime:",
            font=('Helvetica', 10), fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_panel']
        ).pack(anchor='w')

        self.uptime_label = tk.Label(
            session_frame, text="00:00:00",
            font=('Helvetica', 18, 'bold'), fg=self.COLORS['accent_cyan'],
            bg=self.COLORS['bg_panel']
        )
        self.uptime_label.pack(anchor='w')

        tk.Label(
            session_frame, text="Commands Processed:",
            font=('Helvetica', 10), fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_panel']
        ).pack(anchor='w', pady=(10, 0))

        self.commands_label = tk.Label(
            session_frame, text="0",
            font=('Helvetica', 18, 'bold'), fg=self.COLORS['accent_cyan'],
            bg=self.COLORS['bg_panel']
        )
        self.commands_label.pack(anchor='w')

        # Separator
        sep2 = tk.Frame(parent, bg=self.COLORS['border'], height=1)
        sep2.pack(fill='x', padx=15, pady=(5, 15))

        # System vitals
        vitals_title = tk.Label(
            parent, text="SYSTEM VITALS",
            font=('Helvetica', 10, 'bold'), fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_panel']
        )
        vitals_title.pack(anchor='w', padx=15)

        self.vitals_frame = tk.Frame(parent, bg=self.COLORS['bg_panel'])
        self.vitals_frame.pack(fill='x', padx=15, pady=10)

        # Create vital indicators
        self.battery_bar = self._create_vital_bar(self.vitals_frame, "POWER", 0)
        self.cpu_bar = self._create_vital_bar(self.vitals_frame, "CPU", 0)
        self.memory_bar = self._create_vital_bar(self.vitals_frame, "MEMORY", 0)

    def _create_vital_bar(self, parent, label, value):
        """Create a system vital progress bar."""
        frame = tk.Frame(parent, bg=self.COLORS['bg_panel'])
        frame.pack(fill='x', pady=5)

        tk.Label(
            frame, text=label,
            font=('Helvetica', 9), fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_panel'], width=8, anchor='w'
        ).pack(side='left')

        # Progress bar canvas
        canvas = tk.Canvas(
            frame, width=150, height=12,
            bg=self.COLORS['bg_dark'], highlightthickness=0
        )
        canvas.pack(side='left', padx=5)

        # Value label
        value_label = tk.Label(
            frame, text=f"{value}%",
            font=('Helvetica', 9, 'bold'), fg=self.COLORS['accent_cyan'],
            bg=self.COLORS['bg_panel'], width=5
        )
        value_label.pack(side='left')

        return {'canvas': canvas, 'label': value_label}

    def _update_vital_bar(self, bar_dict, value):
        """Update a vital bar's display."""
        canvas = bar_dict['canvas']
        label = bar_dict['label']

        # Determine color based on value
        if value < 60:
            color = self.COLORS['success']
        elif value < 85:
            color = self.COLORS['warning']
        else:
            color = self.COLORS['error']

        # Clear and redraw
        canvas.delete('all')
        width = int(150 * value / 100)
        canvas.create_rectangle(0, 0, width, 12, fill=color, outline='')

        label.config(text=f"{value:.0f}%")

    def _create_conversation_panel(self, parent):
        """Create the conversation/log panel."""
        # Title
        title = tk.Label(
            parent, text="COMMUNICATION LOG",
            font=('Helvetica', 12, 'bold'), fg=self.COLORS['accent_gold'],
            bg=self.COLORS['bg_panel']
        )
        title.pack(pady=(15, 10))

        # Separator
        sep = tk.Frame(parent, bg=self.COLORS['border'], height=1)
        sep.pack(fill='x', padx=15)

        # Conversation text area
        text_frame = tk.Frame(parent, bg=self.COLORS['bg_dark'])
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)

        self.conversation_text = tk.Text(
            text_frame,
            font=('Monaco', 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary'],
            insertbackground=self.COLORS['accent_cyan'],
            selectbackground=self.COLORS['accent_blue'],
            wrap='word',
            state='disabled',
            padx=10,
            pady=10
        )
        self.conversation_text.pack(fill='both', expand=True, side='left')

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.conversation_text.yview)
        scrollbar.pack(fill='y', side='right')
        self.conversation_text.config(yscrollcommand=scrollbar.set)

        # Configure text tags for styling
        self.conversation_text.tag_configure('jarvis', foreground=self.COLORS['accent_cyan'])
        self.conversation_text.tag_configure('user', foreground=self.COLORS['accent_gold'])
        self.conversation_text.tag_configure('system', foreground=self.COLORS['text_dim'])
        self.conversation_text.tag_configure('error', foreground=self.COLORS['error'])

        # Listening indicator
        self.listening_frame = tk.Frame(parent, bg=self.COLORS['bg_panel'])
        self.listening_frame.pack(fill='x', padx=15, pady=(0, 15))

        self.listening_indicator = tk.Label(
            self.listening_frame,
            text="● Awaiting wake word...",
            font=('Helvetica', 11),
            fg=self.COLORS['text_dim'],
            bg=self.COLORS['bg_panel']
        )
        self.listening_indicator.pack(side='left')

    def _create_status_bar(self):
        """Create the bottom status bar."""
        status_bar = tk.Frame(self.root, bg=self.COLORS['bg_panel'], height=30)
        status_bar.pack(fill='x', side='bottom')

        # Time
        self.time_label = tk.Label(
            status_bar,
            text="",
            font=('Helvetica', 10),
            fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg_panel']
        )
        self.time_label.pack(side='left', padx=15)

        # Version
        tk.Label(
            status_bar,
            text="JARVIS v3.0 | Stark Industries",
            font=('Helvetica', 10),
            fg=self.COLORS['text_dim'],
            bg=self.COLORS['bg_panel']
        ).pack(side='right', padx=15)

    def _start_update_loops(self):
        """Start background update loops."""
        self._update_clock()
        self._update_vitals()
        self._process_message_queue()

    def _update_clock(self):
        """Update the time display."""
        now = datetime.now()
        self.time_label.config(text=now.strftime("%A, %B %d, %Y - %H:%M:%S"))

        # Update uptime
        delta = now - self.session_start
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.uptime_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        self.root.after(1000, self._update_clock)

    def _update_vitals(self):
        """Update system vitals display."""
        try:
            # Battery
            battery = psutil.sensors_battery()
            if battery:
                self._update_vital_bar(self.battery_bar, battery.percent)
            else:
                self._update_vital_bar(self.battery_bar, 100)

            # CPU
            cpu = psutil.cpu_percent(interval=0)
            self._update_vital_bar(self.cpu_bar, cpu)

            # Memory
            mem = psutil.virtual_memory()
            self._update_vital_bar(self.memory_bar, mem.percent)
        except Exception:
            pass

        self.root.after(2000, self._update_vitals)

    def _process_message_queue(self):
        """Process messages from other threads."""
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()
                if msg_type == 'log':
                    self._append_to_log(msg_data['text'], msg_data.get('tag', 'system'))
                elif msg_type == 'status':
                    self._update_status(msg_data)
                elif msg_type == 'listening':
                    self._update_listening_indicator(msg_data)
        except queue.Empty:
            pass

        self.root.after(100, self._process_message_queue)

    def _append_to_log(self, text, tag='system'):
        """Append text to the conversation log."""
        self.conversation_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_text.insert('end', f"[{timestamp}] ", 'system')
        self.conversation_text.insert('end', f"{text}\n", tag)
        self.conversation_text.see('end')
        self.conversation_text.config(state='disabled')

    def _update_status(self, status):
        """Update the main status indicator."""
        if status == 'online':
            self.status_label.config(text="● ONLINE", fg=self.COLORS['success'])
        elif status == 'listening':
            self.status_label.config(text="● LISTENING", fg=self.COLORS['accent_cyan'])
        elif status == 'speaking':
            self.status_label.config(text="● SPEAKING", fg=self.COLORS['accent_gold'])
        elif status == 'processing':
            self.status_label.config(text="● PROCESSING", fg=self.COLORS['warning'])
        else:
            self.status_label.config(text="● OFFLINE", fg=self.COLORS['error'])

    def _update_listening_indicator(self, is_listening):
        """Update the listening indicator."""
        if is_listening:
            self.listening_indicator.config(
                text="● Listening...",
                fg=self.COLORS['accent_cyan']
            )
        else:
            self.listening_indicator.config(
                text="● Awaiting wake word...",
                fg=self.COLORS['text_dim']
            )

    # Public methods for integration with main.py
    def log_user_command(self, command):
        """Log a user command."""
        self.commands_processed += 1
        self.commands_label.config(text=str(self.commands_processed))
        self.message_queue.put(('log', {'text': f"USER: {command}", 'tag': 'user'}))

    def log_jarvis_response(self, response):
        """Log a JARVIS response."""
        self.message_queue.put(('log', {'text': f"JARVIS: {response}", 'tag': 'jarvis'}))

    def log_system_message(self, message):
        """Log a system message."""
        self.message_queue.put(('log', {'text': message, 'tag': 'system'}))

    def set_status(self, status):
        """Set the current status (online, listening, speaking, processing)."""
        self.message_queue.put(('status', status))

    def set_listening(self, is_listening):
        """Update the listening indicator."""
        self.message_queue.put(('listening', is_listening))

    def run(self):
        """Start the GUI main loop."""
        # Add initial log message
        self.log_system_message("JARVIS interface initialized")
        self.log_jarvis_response("Good evening, sir. All systems are operational.")

        self.root.mainloop()

    def run_in_thread(self):
        """Run the GUI in a separate thread."""
        gui_thread = threading.Thread(target=self.run, daemon=True)
        gui_thread.start()
        return gui_thread


def launch_gui():
    """Launch the JARVIS GUI."""
    gui = JarvisGUI()
    gui.run()


if __name__ == "__main__":
    launch_gui()
