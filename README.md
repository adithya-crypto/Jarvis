# J.A.R.V.I.S.

**Just A Rather Very Intelligent System** - An Iron Man inspired AI assistant for macOS

A voice-activated desktop assistant with cinematic boot sequences, proactive monitoring, and natural conversation capabilities. Built with Python, featuring wake word detection, neural text-to-speech, and Gemini AI.

## Features

### Voice Interaction
- **Wake Word Detection** - Say "Jarvis" to activate (powered by Picovoice Porcupine)
- **Natural Speech Recognition** - Google Speech Recognition for accurate voice commands
- **British Neural Voice** - Microsoft Edge TTS with en-GB-RyanNeural voice
- **Continuous Conversation** - Follow-up commands without repeating wake word

### AI & Intelligence
- **Gemini 2.0 Flash** - Natural language understanding and responses
- **Context Memory** - Remembers conversation history for coherent dialogue
- **JARVIS Personality** - Movie-accurate wit, formality, and British charm
- **Personal Memory** - Remember and recall facts about you

### System Control
- **App Launcher** - Open Chrome, VS Code, Spotify, Terminal, and more
- **Volume Control** - "Set volume to 50%", "Mute", "Unmute"
- **Brightness Control** - Adjust screen brightness by voice
- **System Commands** - Sleep, shutdown, lock screen

### Proactive Monitoring
- **Battery Alerts** - Warns at 20% and 10% battery
- **CPU Monitoring** - Alerts on sustained high usage
- **Memory Tracking** - Notifications when RAM is low
- **Disk Space** - Warnings when storage is running low

### Productivity
- **Timers & Reminders** - "Set a timer for 5 minutes"
- **Web Search** - Search Google or DuckDuckGo by voice
- **Weather** - Get current weather conditions
- **Code Generation** - Generate code snippets with AI
- **Productivity Tracking** - Track active time and sessions
- **Weekly Summaries** - Review your productivity stats

### User Interface
- **Cinematic Boot** - Arc Reactor ASCII art and animated system checks
- **Rich Dashboard** - ANSI-colored terminal display with system vitals
- **Desktop GUI** - Optional Tkinter interface with Iron Man styling

## Installation

### Prerequisites
- macOS (tested on macOS 12+)
- Python 3.8+
- Microphone access
- Internet connection

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/adithya-crypto/Jarvis.git
   cd Jarvis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   cp config/settings.yaml.template config/settings.yaml
   ```

   Edit `config/settings.yaml` and add your API keys:
   - **Gemini API Key** - Get from [Google AI Studio](https://aistudio.google.com/)
   - **Picovoice Access Key** - Get from [Picovoice Console](https://console.picovoice.ai/)

4. **Grant microphone permissions**
   - Go to System Preferences → Security & Privacy → Privacy → Microphone
   - Enable access for Terminal/iTerm

## Usage

### Terminal Mode
```bash
python main.py
```

### GUI Mode
```bash
python jarvis_app.py --gui
```

### Example Commands

| Command | Action |
|---------|--------|
| "Jarvis" | Activate assistant |
| "Open Chrome" | Launch Google Chrome |
| "Search for Python tutorials" | Web search |
| "What's the weather?" | Get weather info |
| "Set volume to 30 percent" | Adjust volume |
| "Set a timer for 10 minutes" | Start countdown |
| "Remember my favorite color is blue" | Save to memory |
| "What's my favorite color?" | Recall from memory |
| "System status" | Show CPU, RAM, battery |
| "Generate a Python function to sort a list" | AI code generation |
| "Goodbye Jarvis" | Shutdown assistant |

### Easter Eggs
- "I am Iron Man"
- "We have a Hulk"
- "Jarvis, are you there?"

## Project Structure

```
jarvis-assistant/
├── main.py                 # Main entry point
├── jarvis_app.py           # App launcher with GUI option
├── requirements.txt        # Python dependencies
├── setup.py                # py2app configuration
├── config/
│   └── settings.yaml       # API keys (gitignored)
├── core/
│   ├── wake_word.py        # Porcupine wake word detection
│   ├── voice_input.py      # Speech recognition
│   ├── speech_output.py    # Edge TTS synthesis
│   ├── gpt_engine.py       # Gemini AI integration
│   ├── command_router.py   # Command parsing & routing
│   └── context_memory.py   # Conversation context
├── automation/
│   ├── app_launcher.py     # Application control
│   ├── mac_control.py      # System commands
│   ├── web_search.py       # Search engines
│   ├── weather.py          # Weather API
│   ├── file_ops.py         # File operations
│   └── codegen_agent.py    # Code generation
├── monitoring/
│   ├── jarvis_monitor.py   # Proactive alerts daemon
│   ├── system_monitor.py   # System stats
│   └── productivity_tracker.py
├── ui/
│   ├── jarvis_face.py      # Terminal UI & boot sequence
│   ├── dashboard.py        # Rich terminal display
│   ├── jarvis_gui.py       # Tkinter desktop GUI
│   └── notifier.py         # macOS notifications
├── memory/
│   └── memory_manager.py   # Personal fact storage
└── tests/
    └── *.py                # 54 unit tests
```

## Building as macOS App

```bash
# Make build script executable
chmod +x build_app.sh

# Build the .app bundle
./build_app.sh
```

The app will be created in `dist/JARVIS.app`

## Running Tests

```bash
pytest tests/ -v
```

## Configuration

### Voice Settings
Edit `core/speech_output.py` to customize:
- `JARVIS_VOICE` - TTS voice (default: en-GB-RyanNeural)
- `JARVIS_RATE` - Speech speed
- `JARVIS_PITCH` - Voice pitch

### Monitoring Thresholds
Edit `monitoring/jarvis_monitor.py`:
- Battery warning levels
- CPU alert threshold
- Memory alert threshold

## Troubleshooting

### Wake word not detecting
- Check microphone permissions in System Preferences
- Verify Picovoice API key in settings.yaml
- Try speaking closer to the microphone

### No audio output
- Check system volume isn't muted
- Verify edge-tts is installed: `pip install edge-tts`
- Check speaker/headphone connection

### Commands not recognized
- Speak clearly after the "Yes sir?" prompt
- Wait for the listening indicator
- Check internet connection for speech recognition

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [Picovoice](https://picovoice.ai/) - Wake word detection
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - Neural voice synthesis
- [Google Gemini](https://ai.google.dev/) - AI language model
- Iron Man / Marvel - Inspiration for JARVIS personality

---

*"At your service, sir."* - J.A.R.V.I.S.
