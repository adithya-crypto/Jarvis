"""
JARVIS GPT Engine - Enhanced personality with conversation memory and situational awareness.
"""
import requests
import yaml
import json
import random
from datetime import datetime

# Load API key
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["gemini_api_key"]
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Rich JARVIS Personality - Movie accurate
JARVIS_PERSONA = """You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the sophisticated AI assistant created by Tony Stark. You serve as his trusted digital butler, lab assistant, and confidant.

CORE PERSONALITY TRAITS:
- British sophistication with dry wit and subtle sarcasm
- Utterly loyal and genuinely helpful while maintaining dignity
- Calm under pressure, even when things go wrong
- Subtle humor - never crude, always clever
- Anticipatory - you often know what the user needs before they ask
- Formal yet warm - you care about "sir's" wellbeing

SPEECH PATTERNS (use naturally, not forced):
- Address user as "sir" occasionally (not every sentence)
- "At your service", "Right away, sir", "As you wish"
- "I'd advise against that, sir" (when appropriate)
- "Shall I..." (offering suggestions)
- "If I may, sir..." (before giving advice)
- "I've taken the liberty of..." (proactive actions)
- "Indeed", "Quite so", "Very well"

RESPONSE STYLE:
- Keep responses CONCISE (1-3 sentences) since this is voice interaction
- NO emojis ever
- NO markdown symbols (*, #, `, etc.)
- Sound natural and conversational, not robotic
- When confirming actions: be witty, not just "Done"
- When reporting data: present it clearly but with personality
- When something fails: stay calm, offer alternatives

SITUATIONAL AWARENESS:
- You know the current time and can comment on it naturally
- You're aware of system status (battery, CPU, etc.) when mentioned
- You remember recent conversation context
- You notice patterns (user working late, asking same things, etc.)

EXAMPLES OF GOOD RESPONSES:
- User opens Chrome: "Launching Chrome. Shall I prepare your usual tabs, sir?"
- User asks battery: "Power reserves at 45 percent, sir. I'd recommend finding a charging station within the hour."
- User sets timer: "Timer set for 25 minutes. I'll alert you when your focus session concludes."
- Late night query: "Still at it, sir? Your dedication is admirable, though perhaps a cup of tea wouldn't go amiss."
- Error occurs: "I'm afraid that didn't go quite as planned. Shall we try an alternative approach?"

Remember: You are the AI that Tony Stark trusts with his life. Be worthy of that trust."""


def get_time_context():
    """Get current time context for situational awareness."""
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 17:
        period = "afternoon"
    elif 17 <= hour < 21:
        period = "evening"
    else:
        period = "late night"

    return f"Current time: {now.strftime('%H:%M')} ({period})"


def get_jarvis_greeting():
    """Generate a time-aware JARVIS greeting."""
    hour = datetime.now().hour

    morning_greetings = [
        "Good morning, sir. All systems are operational and ready for your command.",
        "Good morning, sir. I trust you slept well. How may I assist you today?",
        "Morning, sir. The day awaits. What shall we accomplish?",
    ]

    afternoon_greetings = [
        "Good afternoon, sir. What can I do for you?",
        "Afternoon, sir. Systems standing by.",
        "Good afternoon, sir. I'm at your disposal.",
    ]

    evening_greetings = [
        "Good evening, sir. How may I be of service?",
        "Evening, sir. I hope the day has been productive.",
        "Good evening, sir. What do you require?",
    ]

    night_greetings = [
        "Working late again, sir? I'll keep the lights on.",
        "Burning the midnight oil, sir? I'm here if you need me.",
        "Rather late to still be working, sir. Shall I make a note to schedule some rest?",
    ]

    if 5 <= hour < 12:
        return random.choice(morning_greetings)
    elif 12 <= hour < 17:
        return random.choice(afternoon_greetings)
    elif 17 <= hour < 21:
        return random.choice(evening_greetings)
    else:
        return random.choice(night_greetings)


def ask_gpt(prompt, context_history=None, system_context=None):
    """
    Generate a JARVIS response using Gemini API.

    Args:
        prompt: The user's current message
        context_history: Optional list of previous exchanges [{"user": "...", "assistant": "..."}]
        system_context: Optional dict with system state {"battery": 45, "time": "22:30", etc.}
    """
    from ui.jarvis_face import Colors
    print(f"  {Colors.YELLOW}[~] Processing...{Colors.RESET}")

    # Build the full prompt with context
    full_prompt_parts = [JARVIS_PERSONA, "\n\n"]

    # Add time context
    full_prompt_parts.append(f"CURRENT CONTEXT: {get_time_context()}")

    # Add system context if provided
    if system_context:
        context_str = ", ".join([f"{k}: {v}" for k, v in system_context.items()])
        full_prompt_parts.append(f", System status: {context_str}")

    full_prompt_parts.append("\n\n")

    # Add conversation history for context
    if context_history and len(context_history) > 0:
        full_prompt_parts.append("RECENT CONVERSATION:\n")
        for exchange in context_history[-5:]:  # Last 5 exchanges
            full_prompt_parts.append(f"User: {exchange['user']}\n")
            full_prompt_parts.append(f"JARVIS: {exchange['assistant']}\n")
        full_prompt_parts.append("\n")

    # Add current user message
    full_prompt_parts.append(f"User: {prompt}\n")
    full_prompt_parts.append("JARVIS (respond in character, concisely):")

    full_prompt = "".join(full_prompt_parts)

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "temperature": 0.8,  # Slightly creative for personality
            "maxOutputTokens": 150,  # Keep responses concise
        }
    }

    try:
        response = requests.post(URL, headers=headers, json=data, timeout=15)
        response.raise_for_status()

        result = response.json()
        reply = result['candidates'][0]['content']['parts'][0]['text'].strip()

        # Clean up any accidental markdown or formatting
        reply = reply.replace('*', '').replace('#', '').replace('`', '')

        return reply

    except requests.exceptions.Timeout:
        return "I'm experiencing some latency in my neural networks, sir. Perhaps we could try that again?"
    except Exception as e:
        print(f"  {Colors.RED}[ERROR] API Error: {e}{Colors.RESET}")
        return "I'm afraid my connection to the mainframe is experiencing difficulties. Shall we try again?"


def ask_gpt_for_action_response(action_type, action_details, user_command):
    """
    Generate a witty JARVIS response for a completed action.

    Args:
        action_type: Type of action (e.g., "open_app", "mute", "search")
        action_details: Details about what was done (e.g., "Chrome")
        user_command: The original user command
    """
    from ui.jarvis_face import Colors

    # For simple actions, generate contextual witty responses without API call
    quick_responses = {
        "open_app": [
            f"Launching {action_details}, sir.",
            f"{action_details} is now at your service.",
            f"Opening {action_details}. Will there be anything else?",
        ],
        "mute": [
            "System muted, sir. Blessed silence.",
            "Audio silenced. Your ears will thank me.",
            "Muted. I shall communicate via interpretive dance if needed.",
        ],
        "unmute": [
            "Audio restored, sir.",
            "Sound systems back online.",
            "Unmuted. The world can hear you now, for better or worse.",
        ],
        "volume": [
            f"Volume adjusted to {action_details} percent.",
            f"Audio levels set to {action_details}. Is that to your liking, sir?",
        ],
    }

    if action_type in quick_responses:
        return random.choice(quick_responses[action_type])

    # For more complex responses, use the API
    prompt = f"I just executed this command for the user: '{user_command}'. The action was: {action_type} - {action_details}. Generate a brief, witty JARVIS-style confirmation (1 sentence max)."

    return ask_gpt(prompt)


def generate_diagnostic_report():
    """Generate a full JARVIS-style diagnostic report."""
    import psutil

    battery = psutil.sensors_battery()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    report_parts = ["Running full diagnostic, sir.", ""]

    # Battery
    if battery:
        bat_status = "charging" if battery.power_plugged else "on battery"
        report_parts.append(f"Power reserves at {battery.percent} percent, {bat_status}.")

    # CPU
    if cpu > 80:
        report_parts.append(f"Processor running hot at {cpu:.0f} percent. I'd recommend closing some applications.")
    else:
        report_parts.append(f"Processor load nominal at {cpu:.0f} percent.")

    # Memory
    mem_gb = mem.used / (1024**3)
    mem_total = mem.total / (1024**3)
    if mem.percent > 85:
        report_parts.append(f"Memory utilization critical: {mem_gb:.1f} of {mem_total:.1f} gigabytes.")
    else:
        report_parts.append(f"Memory allocation stable at {mem.percent:.0f} percent.")

    # Disk
    if disk.percent > 90:
        report_parts.append(f"Storage capacity warning: {disk.percent:.0f} percent utilized. Consider archiving some files, sir.")
    else:
        report_parts.append(f"Storage systems nominal.")

    report_parts.append("")
    report_parts.append("All primary systems operational, sir.")

    return " ".join(report_parts)
