import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import signal
import psutil

# A global variable to hold the subprocesses for each script
processes = []

# Function to execute the image object detection script
def run_image_detection():
    # Ask the user whether to use a sample or upload their own file
    choice = messagebox.askquestion("Select Image", "Do you want to use a sample image or upload your own? (Yes for sample, No to upload)")

    if choice == 'yes':
        image_path = 'images/sample.jpg'  # Use the predefined sample image
    else:
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not image_path:
            messagebox.showerror("Error", "No file selected!")
            return
    
    try:
        # Start the subprocess and store it in the processes list
        process = subprocess.Popen(["python", "python/image_object_detection.py", "-i", image_path])
        processes.append(process)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running image detection: {e}")

# Function to execute the video object detection script
def run_video_detection():
    # Ask the user whether to use a sample or upload their own file
    choice = messagebox.askquestion("Select Video", "Do you want to use a sample video or upload your own? (Yes for sample, No to upload)")

    if choice == 'yes':
        video_path = 'videos/sample_video.mp4'  # Use the predefined sample video
    else:
        video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if not video_path:
            messagebox.showerror("Error", "No file selected!")
            return
    
    try:
        # Start the subprocess and store it in the processes list
        process = subprocess.Popen(["python", "python/video_object_detection.py", "-v", video_path])
        processes.append(process)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running video detection: {e}")

# Function to execute the camera object detection script
def run_camera_detection():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to start camera detection?")
    if result == 'yes':
        try:
            # Start the subprocess and store it in the processes list
            process = subprocess.Popen(["python", "python/cam_object_detection.py"])
            processes.append(process)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error running camera detection: {e}")

# Function to terminate all subprocesses
def terminate_processes():
    for process in processes:
        try:
            # Terminate each process by sending SIGTERM signal
            process.terminate()
            process.wait()
        except Exception as e:
            print(f"Error terminating process: {e}")

# Function that runs when the window is closed
def on_close():
    terminate_processes()
    root.quit()

# Create the main tkinter window
root = tk.Tk()
root.title("Futuristic Object Detection")
root.geometry("600x400")  # Set the window size
root.configure(bg="#1a1a1a")  # Set background color

# Title label
title_label = tk.Label(root, text="Object Detection GUI", font=("Helvetica", 30, "bold"), fg="#f0f0f0", bg="#1a1a1a")
title_label.pack(pady=30)

# Create buttons with futuristic styling
button_style = {
    "font": ("Arial", 14, "bold"),
    "bg": "#007bff",
    "fg": "white",
    "width": 20,
    "height": 2,
    "bd": 0,
    "relief": "flat",
    "activebackground": "#0056b3",
    "activeforeground": "white",
}

# Image Object Detection Button
image_button = tk.Button(root, text="Image Detection", **button_style, command=run_image_detection)
image_button.pack(pady=10)

# Video Object Detection Button
video_button = tk.Button(root, text="Video Detection", **button_style, command=run_video_detection)
video_button.pack(pady=10)

# Camera Object Detection Button
camera_button = tk.Button(root, text="Camera Detection", **button_style, command=run_camera_detection)
camera_button.pack(pady=10)

# Handle the close event to terminate subprocesses before quitting
root.protocol("WM_DELETE_WINDOW", on_close)

# Run the tkinter event loop
root.mainloop()
