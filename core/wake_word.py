import pvporcupine
import struct
import pyaudio
import yaml
import time
import speech_recognition as sr

def get_microphone_index():
    """Get the best available microphone index."""
    mic_names = sr.Microphone.list_microphone_names()
    
    # Priority 1: AirPods
    for index, name in enumerate(mic_names):
        if "AirPods" in name:
            print(f"🎙️ Wake word using: {name} (Index {index})")
            return index
    
    # Priority 2: MacBook Pro
    for index, name in enumerate(mic_names):
        if "MacBook Pro Microphone" in name:
            print(f"🎙️ Wake word using: {name} (Index {index})")
            return index
    
    print("🎙️ Wake word using: default microphone")
    return None  # None means use default

def wait_for_wake_word():
    """
    Listen for the wake word 'Jarvis' using Porcupine.
    Returns True when wake word is detected.
    """
    porcupine = None
    audio_stream = None
    pa = None
    
    try:
        # Load access key from config
        with open("config/settings.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        access_key = config.get("picovoice_access_key")
        if not access_key or access_key == "YOUR_PICOVOICE_ACCESS_KEY_HERE":
            print("❌ Picovoice access key not configured!")
            print("📝 Please get a free key from: https://console.picovoice.ai/")
            print("📝 Then add it to config/settings.yaml")
            return False
        
        # Initialize Porcupine with built-in 'jarvis' keyword
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=['jarvis']
        )
        
        # Get the best microphone
        mic_index = get_microphone_index()
        
        # Initialize PyAudio
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("👂 Listening for wake word 'Jarvis'...")
        
        while True:
            # Read audio frame
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            # Check for wake word
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("✅ Wake word detected!")
                return True
                
    except Exception as e:
        print(f"❌ Wake word error: {e}")
        return False
        
    finally:
        # Cleanup - release audio resources
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()
        # Brief pause to allow audio system to fully release
        # before voice input opens its own microphone stream
        time.sleep(0.2)
