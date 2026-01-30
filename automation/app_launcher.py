import subprocess

def open_app(app_name):
    print(f"🚀 Launching {app_name}...")
    subprocess.run(["open", "-a", app_name])
