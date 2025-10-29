#!/usr/bin/env python3

import subprocess
import tkinter as tk
from tkinter import messagebox

# Function to start the VPN connection
def start_vpn():
    try:
        global process
        # Run the Bash script as a subprocess
        process = subprocess.Popen(
            [
                "/run/current-system/sw/bin/bash", "-c",
                """sudo openconnect --protocol=nc https://duosslvpn.medical.washington.edu << EOF
jflana
AM1dnigh7Dr3ary
push
EOF
"""
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Notify the user
        status_label.config(text="Connected. Close the window to disconnect.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start VPN: {e}")

# Function to stop the VPN connection
def stop_vpn():
    if process:
        process.terminate()  # Terminate the process
    root.destroy()  # Close the GUI window

# Create the Tkinter GUI
root = tk.Tk()
root.title("VPN Connector")

# Add a label to show status
status_label = tk.Label(root, text="Click 'Connect' to start VPN.", padx=10, pady=10)
status_label.pack()

# Add a button to connect
connect_button = tk.Button(root, text="Connect", command=start_vpn, padx=10, pady=5)
connect_button.pack()

# Add a close button
close_button = tk.Button(root, text="Close", command=stop_vpn, padx=10, pady=5)
close_button.pack()

# Run the GUI event loop
root.mainloop()
