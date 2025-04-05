#!/usr/bin/env python3
import os
import subprocess
import json
from playwright.sync_api import sync_playwright

# Create directories if they don't exist
profile_dir = "/home/toby/openmanus_browser_profiles/jupiter"
os.makedirs(profile_dir, exist_ok=True)

# Create empty storage state file if it doesn't exist
storage_state_path = os.path.join(profile_dir, "storage_state.json")
if not os.path.exists(storage_state_path):
    with open(storage_state_path, "w") as f:
        json.dump({"cookies": [], "origins": []}, f)

# Set environment variables for browser_use
os.environ["BROWSER_USE_PERSISTENT_CONTEXT"] = "true"
os.environ["BROWSER_USE_STORAGE_STATE"] = storage_state_path

# Launch persistent browser context
with sync_playwright() as p:
    # Launch persistent context
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        headless=False,
        args=[
            "--profile-directory=Profile1",
            "--enable-features=NetworkService",
            "--disable-features=IsolateOrigins,site-per-process"
        ]
    )

    # Save storage state for future sessions
    browser.storage_state(path=storage_state_path)

    # Get first page from context
    page = browser.pages[0]

    # Launch OpenManus in a separate process
    process = subprocess.Popen(["python3", "main.py"])

    try:
        while process.poll() is None:
            pass
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        process.terminate()
        try:
            # Save final state before closing
            browser.storage_state(path=storage_state_path)
            browser.close()
        except Exception as e:
            print(f"Error saving browser state: {e}")
        process.wait()
