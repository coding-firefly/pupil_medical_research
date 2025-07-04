# Gaze Tracking for ADHD Diagnosis

---

## Overview

This application is designed to provide insights into potential ADHD markers by tracking a participant's gaze while they are presented with distractions. It's built to be used by **healthcare professionals** as an aid in the diagnostic process.

## Features

* Iris-center calibration and a fixed 60-second tracking session.
* Real-time gaze tracking of the left iris using MediaPipe Face Mesh.
* Live feedback showing the current iris x-position versus the calibrated center.
* Drift detection beyond ±15 px tolerance around the calibrated center.
* Automatic logging of each drift event’s direction (“Attention_towards_Left” or “Attention_towards_Right”) and duration.
* Distraction integration with looping piano background music and a “fly” surprise sound effect triggered on drift (0.5 % chance per frame).
* Post-session drift analysis: a detailed textual log plus a bar-chart visualization of all recorded drift events.

---

## Target Market

This application is specifically developed for **healthcare providers** to assist them in the diagnosis of ADHD.

---

## Tech Stack

The gaze tracking functionality, which is a core component, is implemented in Python and leverages the following key dependencies:

### Python Dependencies

* **Flet**: Provides a simple, Flutter-inspired UI framework for the Python components.
* **OpenCV-Python**: Handles camera capture and frame processing for video input.
* **MediaPipe**: Utilized for precise iris landmark detection, enabling accurate gaze tracking.
* **Pygame**: Manages audio playback for background music and sound effects.

### Repository Structure

```

frontend/
main.py                       \# Core application logic, UI layout, and real-time iris tracking code.
music/
piano\_bgm.mp3             \# Background loop during tracking sessions.
fly.mp3                   \# Surprise sound effect triggered on drift detection.
requirements.txt              \# Lists all Python dependencies.

````

### Key Components & Logic (main.py)

* **Configuration & Global Variables**:
    * `camera_slot`: Index of the webcam (default: `0`).
    * `minimum_detection_confidence`, `minimum_tracking_confidence`: Thresholds for MediaPipe landmark reliability.
    * `threshold_x`: Pixel tolerance around the calibrated center for drift detection.
    * `generation_rate`: Probability per frame that a "surprise" sound plays when drift occurs.
    * **Global Containers**:
        * `calibration_coords`: Stores the calibrated center (x, threshold) of the iris.
        * `iris_drift`: A list to record details of each drift event (direction and duration).

* **Core Functions**:
    * `play_background_music()`: Initializes Pygame mixer, loads, and loops `piano_bgm.mp3` until tracking stops, fading out at the session end.
    * `surprise()`: Plays `fly.mp3` once when drift is detected. Includes a placeholder for random pan simulation.
    * `iris_position(frame)`: Converts BGR frames to RGB, runs MediaPipe Face Mesh, and returns the pixel (x, y) coordinates of the left iris center or `(None, None)` if not detected.
    * `track_iris(live_update, update_log, update_pos)`: Captures video for a fixed duration (60 seconds) or until stopped. For each frame, it computes the iris x-position, compares it to the calibrated center, marks drift events (start/end, direction, duration), and occasionally triggers `surprise()` based on `generation_rate`. Upon completion, it calls back to update UI logs and chart visualization.

* **User Interface (Flet)**:
    * **Instruction Panel**: Explains the purpose, procedure, and controls of the application.
    * **Control Panel**: Contains buttons for:
        * **Calibrate**: Captures the initial iris center.
        * **Start**: Initiates the 60-second tracking session, background music, and drift logging.
        * **Stop**: Halts tracking mid-test.
    * **Live Feedback**: Displays the current iris position relative to the calibrated center.
    * **Drift Log & Chart**: Provides a textual log of each drift event and a bar chart visualizing the duration and direction of drifts.

---

## Usage Instructions

To set up and run the application, follow these steps:

1.  **Install Dependencies**:
    ```bash
    pip install -r frontend/req.txt
    ```

2.  **Webcam Connection**:
    Ensure a working webcam is connected to your system. The project defaults to using device `0`.

3.  **Run the Application**:
    Navigate to the `frontend/` directory in your terminal and execute:
    ```bash
    flet -r main.py
    ```

4.  **Follow On-Screen Instructions**:
    * Sit straight and focus directly on the camera.
    * Click the "**Calibrate**" button.
    * Then, click the "**Start**" button to begin the gaze tracking session.
    * Observe the drift log and bar chart for analysis once the session is complete.
