"""
Setup script for building JARVIS as a macOS application.
Usage: python setup.py py2app
"""
from setuptools import setup

APP = ['jarvis_app.py']
DATA_FILES = [
    ('config', ['config/settings.yaml']),
    ('memory', ['memory/user_profile.json']),
    ('behaviors', [
        'behaviors/study_mode.xml',
        'behaviors/morning_routine.xml',
        'behaviors/focus_routine.xml',
        'behaviors/code_session.xml',
        'behaviors/job_search.xml',
    ]),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Add path to .icns file if you have one
    'plist': {
        'CFBundleName': 'JARVIS',
        'CFBundleDisplayName': 'J.A.R.V.I.S.',
        'CFBundleIdentifier': 'com.stark.jarvis',
        'CFBundleVersion': '3.0.0',
        'CFBundleShortVersionString': '3.0',
        'NSMicrophoneUsageDescription': 'JARVIS needs microphone access for voice commands.',
        'NSSpeechRecognitionUsageDescription': 'JARVIS uses speech recognition for voice commands.',
        'LSMinimumSystemVersion': '10.15',
        'NSHighResolutionCapable': True,
    },
    'packages': [
        'core',
        'automation',
        'memory',
        'logic',
        'monitoring',
        'ui',
        'auth',
    ],
    'includes': [
        'tkinter',
        'speech_recognition',
        'psutil',
        'yaml',
        'requests',
        'pvporcupine',
    ],
    'excludes': ['test', 'tests'],
}

setup(
    name='JARVIS',
    version='3.0.0',
    description='Just A Rather Very Intelligent System - Iron Man AI Assistant',
    author='Stark Industries',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
