# setup.py

from setuptools import setup

APP = ['ui.py']
DATA_FILES = ['icon.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['torch', 'whisper', 'better_profanity'],
    'plist': {
        'CFBundleName': 'Profanity Tagger',
        'CFBundleDisplayName': 'Profanity Tagger',
        'CFBundleIdentifier': 'com.local.ProfanityTagger',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'LSBackgroundOnly': True  # Keeps it hidden (optional)
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
