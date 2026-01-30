"""
JARVIS Voice Input - Speech recognition with microphone selection.
Optimized for smooth command recognition after wake word.
"""
import speech_recognition as sr

# Cache the microphone to avoid repeated lookups
_cached_mic_index = None
_cached_recognizer = None


def get_microphone():
    """Find AirPods or MacBook Pro Microphone, or return default."""
    global _cached_mic_index

    if _cached_mic_index is not None:
        return sr.Microphone(device_index=_cached_mic_index)

    mic_names = sr.Microphone.list_microphone_names()

    # Priority 1: AirPods
    for index, name in enumerate(mic_names):
        if "AirPods" in name:
            print(f"  [Mic] Using: {name}")
            _cached_mic_index = index
            return sr.Microphone(device_index=index)

    # Priority 2: MacBook Pro
    for index, name in enumerate(mic_names):
        if "MacBook Pro Microphone" in name:
            print(f"  [Mic] Using: {name}")
            _cached_mic_index = index
            return sr.Microphone(device_index=index)

    # Default
    print("  [Mic] Using: Default")
    return sr.Microphone()


def get_recognizer():
    """Get a cached recognizer with optimized settings."""
    global _cached_recognizer

    if _cached_recognizer is None:
        _cached_recognizer = sr.Recognizer()
        # Optimized settings for responsiveness
        _cached_recognizer.energy_threshold = 400  # Slightly higher to avoid noise
        _cached_recognizer.dynamic_energy_threshold = True
        _cached_recognizer.dynamic_energy_adjustment_damping = 0.15
        _cached_recognizer.dynamic_energy_ratio = 1.5
        _cached_recognizer.pause_threshold = 0.8  # Shorter pause = faster response
        _cached_recognizer.phrase_threshold = 0.3
        _cached_recognizer.non_speaking_duration = 0.5

    return _cached_recognizer


def listen_to_command(timeout=10, phrase_time_limit=15):
    """
    Listen for a voice command.

    Args:
        timeout: How long to wait for speech to start (seconds)
        phrase_time_limit: Max duration of the phrase (seconds)

    Returns:
        The recognized text, or None if nothing detected.
    """
    from ui.jarvis_face import Colors

    recognizer = get_recognizer()

    try:
        with get_microphone() as source:
            # Quick ambient noise adjustment - don't make it too long
            # or it will cut off the beginning of speech
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print(f"  {Colors.CYAN}[*] Listening...{Colors.RESET}")

            # Listen with specified timeouts
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        print(f"  {Colors.DIM}[Processing speech...]{Colors.RESET}")

        # Recognize using Google
        command = recognizer.recognize_google(audio)
        print(f"  {Colors.WHITE}Heard: \"{command}\"{Colors.RESET}")
        return command

    except sr.WaitTimeoutError:
        print(f"  {Colors.DIM}[No speech detected - timeout]{Colors.RESET}")
        return None
    except sr.UnknownValueError:
        print(f"  {Colors.YELLOW}[Could not understand - please repeat]{Colors.RESET}")
        return None
    except sr.RequestError as e:
        print(f"  {Colors.RED}[ERROR] Speech service unavailable: {e}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"  {Colors.RED}[ERROR] Voice input: {e}{Colors.RESET}")
        return None


def listen_quick(timeout=4, phrase_time_limit=8):
    """
    Quick listen for follow-up commands - shorter timeouts.
    """
    return listen_to_command(timeout=timeout, phrase_time_limit=phrase_time_limit)


def list_microphones():
    """List all available microphones."""
    mic_names = sr.Microphone.list_microphone_names()
    print("\nAvailable Microphones:")
    for index, name in enumerate(mic_names):
        print(f"  [{index}] {name}")
    return mic_names


def test_microphone():
    """Test the microphone by recording a short sample."""
    from ui.jarvis_face import Colors

    print(f"\n{Colors.CYAN}Testing microphone...{Colors.RESET}")
    print("Speak something when prompted.\n")

    result = listen_to_command(timeout=5, phrase_time_limit=5)

    if result:
        print(f"\n{Colors.GREEN}Success! Recognized: \"{result}\"{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}Failed to recognize speech.{Colors.RESET}")
        print("Tips:")
        print("  - Speak louder and closer to the microphone")
        print("  - Reduce background noise")
        print("  - Try using AirPods or headset with mic")

    return result
