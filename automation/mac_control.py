import subprocess
import psutil

def mute_system():
    subprocess.run(["osascript", "-e", 'set volume output muted true'])

def unmute_system():
    subprocess.run(["osascript", "-e", 'set volume output muted false'])

def set_volume(level):
    """Set volume to a specific level (0-100)."""
    # AppleScript volume is 0-7 usually, or 0-100 with output volume
    subprocess.run(["osascript", "-e", f'set volume output volume {level}'])

def set_brightness(level):
    """Set brightness (0.0-1.0). Note: This might require 'brightness' brew package or similar, 
    but standard osascript for brightness is tricky without external tools. 
    We'll try a common approach or just log it if not easily possible without extra tools."""
    # Using 'brightness' command line tool if available, otherwise this is hard on stock mac
    # For now, let's just print as a placeholder if we don't want to install 'brightness' via brew
    print(f"🔆 Setting brightness to {level} (requires 'brightness' tool installed)")
    # subprocess.run(["brightness", str(level)]) 

def speak_system_status():
    battery = psutil.sensors_battery()
    status_msg = ""
    if battery:
        status_msg += f"Battery is at {battery.percent}%."
        if battery.power_plugged:
            status_msg += " Charging."
        else:
            status_msg += " Not plugged in."
    else:
        status_msg += "Battery info not available."
    
    return status_msg
