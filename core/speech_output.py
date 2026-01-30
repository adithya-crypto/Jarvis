"""
JARVIS Speech Output - High-quality British voice synthesis with Iron Man style.
"""
import os
import subprocess
import time
import re
import shutil


# JARVIS voice configuration
JARVIS_VOICE = "en-GB-RyanNeural"  # British male neural voice
JARVIS_RATE = "+0%"  # Speech rate adjustment
JARVIS_PITCH = "+0Hz"  # Pitch adjustment


def _clean_text_for_speech(text):
    """
    Clean text for natural speech synthesis.
    Removes markdown, emojis, and formats numbers/abbreviations.
    """
    # Remove markdown formatting
    clean = text.replace("*", "").replace("#", "").replace("`", "").replace("_", " ")

    # Remove emojis and special characters (keep alphanumeric, spaces, punctuation)
    clean = re.sub(r'[^\w\s,?.!\'\"\-\:\;\(\)%]', '', clean)

    # Fix common abbreviations for better pronunciation
    clean = clean.replace("vs.", "versus")
    clean = clean.replace("etc.", "etcetera")
    clean = clean.replace("e.g.", "for example")
    clean = clean.replace("i.e.", "that is")

    # Make percentages sound natural
    clean = re.sub(r'(\d+)%', r'\1 percent', clean)

    # Make file sizes sound natural
    clean = re.sub(r'(\d+\.?\d*)\s*GB', r'\1 gigabytes', clean)
    clean = re.sub(r'(\d+\.?\d*)\s*MB', r'\1 megabytes', clean)
    clean = re.sub(r'(\d+\.?\d*)\s*KB', r'\1 kilobytes', clean)

    # Clean up multiple spaces
    clean = re.sub(r'\s+', ' ', clean).strip()

    return clean


def _get_edge_tts_path():
    """Get the path to edge-tts executable."""
    path = shutil.which("edge-tts")
    if path:
        return path
    # Fallback paths
    fallbacks = [
        "/Users/adithyasriramoju/.pyenv/versions/3.8.18/bin/edge-tts",
        "/usr/local/bin/edge-tts",
        os.path.expanduser("~/.local/bin/edge-tts"),
    ]
    for fb in fallbacks:
        if os.path.exists(fb):
            return fb
    return "edge-tts"  # Hope it's in PATH


def speak(text, rate=JARVIS_RATE, pitch=JARVIS_PITCH):
    """
    Speak text using JARVIS voice (Microsoft Edge TTS Neural).

    Args:
        text: The text to speak
        rate: Speech rate (e.g., "+10%", "-5%")
        pitch: Voice pitch (e.g., "+5Hz", "-10Hz")
    """
    from ui.jarvis_face import Colors

    # Clean text for speech
    clean_text = _clean_text_for_speech(text)

    if not clean_text:
        return

    # Display indicator
    print(f"  {Colors.GREEN}[>] Speaking: {clean_text[:60]}{'...' if len(clean_text) > 60 else ''}{Colors.RESET}")

    try:
        edge_tts_path = _get_edge_tts_path()
        output_file = "/tmp/jarvis_response.mp3"

        # Build edge-tts command with voice parameters
        cmd = [
            edge_tts_path,
            "--voice", JARVIS_VOICE,
            "--rate", rate,
            "--pitch", pitch,
            "--text", clean_text,
            "--write-media", output_file
        ]

        # Generate audio
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Fix for Bluetooth/AirPods:
        # Force volume to reasonable level to prevent "0 volume" issue
        subprocess.run(
            ["osascript", "-e", "set volume output volume 50"],
            capture_output=True
        )

        # Brief pause for Bluetooth profile switch (HFP -> A2DP)
        time.sleep(0.15)

        # Play audio using macOS native player
        subprocess.run(["afplay", output_file], check=True)

        # Brief pause after playback to let Bluetooth audio profile settle
        # This prevents the mic from cutting off the start of the next listen
        time.sleep(0.3)

        # Clean up temp file
        if os.path.exists(output_file):
            os.remove(output_file)

    except subprocess.CalledProcessError as e:
        print(f"  {Colors.RED}[ERROR] TTS generation failed: {e}{Colors.RESET}")
    except FileNotFoundError:
        print(f"  {Colors.RED}[ERROR] edge-tts not found. Install with: pip install edge-tts{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}[ERROR] Speech error: {e}{Colors.RESET}")


def speak_urgent(text):
    """Speak with slightly faster rate for urgent messages."""
    speak(text, rate="+10%")


def speak_slow(text):
    """Speak with slower rate for important information."""
    speak(text, rate="-10%")


def speak_greeting(text):
    """Speak a greeting with warm tone."""
    speak(text, rate="-5%", pitch="+2Hz")


def play_sound(sound_name):
    """
    Play a system sound effect.

    Args:
        sound_name: Name of sound ("chime", "alert", "error")
    """
    sounds = {
        "chime": "/System/Library/Sounds/Glass.aiff",
        "alert": "/System/Library/Sounds/Sosumi.aiff",
        "error": "/System/Library/Sounds/Basso.aiff",
        "success": "/System/Library/Sounds/Blow.aiff",
        "pop": "/System/Library/Sounds/Pop.aiff",
    }

    sound_path = sounds.get(sound_name)
    if sound_path and os.path.exists(sound_path):
        try:
            subprocess.run(["afplay", sound_path], capture_output=True)
        except Exception:
            pass  # Silently fail if sound can't play


def test_voice():
    """Test the JARVIS voice system."""
    speak("JARVIS voice systems online. All neural speech pathways are functioning normally, sir.")
