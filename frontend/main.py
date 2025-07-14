import flet as ft
import cv2
import mediapipe as mp
import threading
import time
import pygame
import os
import random

#__General Settings
camera_slot = 0
minimum_detection_confidence = 0.3
minimum_tracking_confidence = 0.3
threshold_x = 15
generation_rate = 0.005

#__Global Var
iris_drift = []
calibration_coords = None
drift_start_time = None
stop_tracking = False

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=minimum_detection_confidence,
    min_tracking_confidence=minimum_tracking_confidence
)

def play_background_music():
    try:
        pygame.mixer.init()
        bgm_path = os.path.join(os.path.dirname(__file__), "music", "piano_bgm.mp3")
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  
        print("[BGM] Piano background started")

        while not stop_tracking:
            time.sleep(0.5)

        pygame.mixer.music.fadeout(2000)
        print("[BGM] Fading out Triggered")
    except Exception as e:
        print(f"[BGM] Error {e}")

def surprise():
    try:
        fly_path = os.path.join(os.path.dirname(__file__), "music", "fly.mp3")
        fly_sound = pygame.mixer.Sound(fly_path)
        pan = random.choice(["left", "right"])
        if pan == "left":
            fly_sound.set_volume(0.5)
        else:
            fly_sound.set_volume(0.5)

        fly_sound.play()
        print(f"[Fly] Summoned !!")

        time.sleep(2) 
    except Exception as e:
        print(f"[Sound Error] {e}")

def iris_position(frame):
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            center_left_iris = face_landmarks.landmark[474]
            x = int(center_left_iris.x * w)
            y = int(center_left_iris.y * h)
            return x, y
    return None, None

def track_iris(live_update, update_log, update_pos):
    global drift_start_time, stop_tracking
    cap = cv2.VideoCapture(camera_slot)
    start = time.time()
    duration = 60

    while time.time() - start < duration and not stop_tracking:
        try:
            ret, frame = cap.read()
            if not ret:
                break

            pos = iris_position(frame)
            if pos is not None and calibration_coords:
                x, _ = pos
                cx, threshold = calibration_coords

                update_pos(f"Iris Live Pos At {x}, Threshold = +/-{threshold}")
                #print(f"Iris X = {x}, Center = {cx}, Threshold = ±{threshold}")
                
                if x is not None:
                    if abs(x - cx) > threshold:
                        if drift_start_time is None:
                            drift_start_time = time.time()
                        else:
                             pass
                        # 🔴 Animate drift_dot to red (visual alert)
                        #drift_dot.bgcolor = "#FF5555"
                        #drift_dot.update()
                    else:
                        if drift_start_time:
                            drift_duration = round((time.time() - drift_start_time), 2)
                            direction = "Attention_towards_Left" if x > cx else "Attention_towards_Right"
                            iris_drift.append({
                                "direction": direction,
                                "duration": drift_duration
                            })
                            drift_start_time = None

                            # 🟢 Back to center – show green again
                        # drift_dot.bgcolor = "#00FF00"
                        # drift_dot.update()
                try:
                    alignment = x - cx
                    attempt_alignment = max(-145, min(alignment, 145))
                    drift_dot.left = 150 + attempt_alignment
                except:
                    pass
        except:
            pass

        #__Sound
        if random.random() < generation_rate:  
            threading.Thread(target=surprise).start()

    cap.release()
    cv2.destroyAllWindows()
    update_pos("")
    live_update("Tracking Complete")
    update_log()

#__Main
def main(page: ft.Page):
    page.title = "ADHD Tester"
    page.scroll = ft.ScrollMode.AUTO

    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.padding.symmetric(horizontal=32, vertical=24)

    status = ft.Text("Pending Iris Calibration")
    drift_log = ft.Text("")
    iris_position_text = ft.Text("")
    instruction_text = ft.Text(
    """📘 ADHD Visual Attention Assessment

    This tool helps assess attention drift patterns associated with ADHD through real-time tracking of the left iris.

    📋 Procedure:
    1. Sit upright and focus on the center of the screen or directly into the camera.
    2. Click “Calibrate” to capture your visual center.
    3. Once calibrated, click “Start” to begin the 60-second tracking session.
    4. You may stop the test anytime by clicking “Stop.” Otherwise, it will conclude automatically after 60 seconds.

    Throughout the session, maintain your gaze on the calibrated center. Drift events will be recorded for analysis.""",
    size=13,
    color=ft.Colors.BLUE_GREY_100,
    text_align=ft.TextAlign.LEFT,
    )

    def calibrate(e):
        cap = cv2.VideoCapture(camera_slot)
        time.sleep(1)
        ret, frame = cap.read()
        cap.release()

        if ret:
            x, _ = iris_position(frame)
            if x:
                global calibration_coords
                calibration_coords = (x, threshold_x) 
                status.value = f"Left Iris Calibrated at x-Axis: {x}"
            else:
                status.value = "Calibration Failed, Left Iris not Detected"
        else:
            status.value = "Camera Kaputt for sure"
        page.update()

    def start_tracking(e):
        global stop_tracking

        stop_tracking = False
        feedback.controls.clear()
        feedback.controls.append(ft.Text("", color=ft.Colors.GREEN_ACCENT))

        drift_log.value = ""
        iris_drift.clear()

        threading.Thread(target=play_background_music, daemon=True).start()
        lane_display.visible = True
        counter_balance.visible = True

        page.update()
        threading.Thread(target=track_iris, args=(
            lambda msg: update_feedback(msg),
            update_logs,
            update_position
        )).start()


    def update_feedback(msg):
        feedback.controls.clear()
        feedback.controls.append(ft.Text(f"{msg}", color=ft.Colors.GREEN_ACCENT))

        page.update()

    def update_logs():
        # logs = "\n".join([f"{'[Serious]\n' if d['duration']>2.5 else ""}{d['direction']} for {d['duration']}s" for d in iris_drift])
        logs = "\n".join([("[Serious]\n" if d['duration'] > 2.5 else "") + f"{d['direction']} for {d['duration']}s" for d in iris_drift])

        drift_log.value = logs or "Perfect!! No Drift at all!!"
        global stop_tracking 
        stop_tracking = True

        lane_display.visible = False 
        counter_balance.visible = False
        feedback.controls.clear()

        if not iris_drift:
            feedback.controls.append(ft.Text("Perfect!! No Drift at all!!", color=ft.Colors.GREEN_ACCENT))
        else:
            chart_data = []
            for i, entry in enumerate(iris_drift):
                value = round(entry["duration"], 2)
                if value>3:
                    value = 3
                bar_value = ft.BarChartRod(
                    from_y=0,
                    to_y=value if entry["direction"] == "Attention_towards_Left" else -value,
                    width=14,
                    color=ft.Colors.AMBER,
                    border_radius=4
                )
                chart_data.append(ft.BarChartGroup(x=i, bar_rods=[bar_value]))

            feedback.controls.append(
                ft.BarChart(
                    expand=True,
                    bar_groups=chart_data,
                    left_axis=ft.ChartAxis(
                        title=ft.Text("Duration (s)"),
                        title_size=20,
                        labels_interval=1,
                    ),
                    bottom_axis=ft.ChartAxis(
                        title=ft.Text("Drift Index L/R"),
                        title_size=20
                    ),
                    horizontal_grid_lines=ft.ChartGridLines(interval=1),
                    min_y=-3,
                    max_y=3,
                    tooltip_bgcolor=ft.Colors.BLUE_GREY_900,
                    interactive=True
                )
            )

        #_EO_Graph
        page.update()

    def update_position(msg):
        iris_position_text.value = msg
        page.update()

    def stop_tracking_btn(e):
        print("stop tracking clicked")
        global stop_tracking
        stop_tracking = True
        update_feedback("Tracking stopped.")

    title = ft.Text(
        "ADHD Iris Tracking Assessment",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,  # Deep blue for title
        text_align=ft.TextAlign.CENTER,
    )

    subtitle = ft.Text(
        "Visual Attention Drift Monitor – Calibrate, Track, Review",
        size=16,
        italic=True,
        color=ft.Colors.BLUE_GREY_200,
        text_align=ft.TextAlign.CENTER,
    )

    status = ft.Text(color=ft.Colors.BLUE_700)
    feedback = ft.Column()
    drift_log_label = ft.Text("📋 Drift Log", size=16, weight="bold", color=ft.Colors.BLUE_GREY_100)
    iris_position_text = ft.Text(color=ft.Colors.LIGHT_BLUE_ACCENT)
    
    global counter_balance
    counter_balance = ft.Text("Visual Counter-Balance on X Axis", visible= False)
    global drift_dot
    # drift_dot = ft.Container(width=10, height=30, bgcolor="#00FF00", left=150)
    drift_dot = ft.Container(
    width=10,
    height=30,
    bgcolor="#00FF00",
    left=150,
    animate_position=300,     # milliseconds
    border_radius=4
)

    global lane_display
    lane_display = ft.Container(
        content=ft.Stack([
            ft.Container(width=300, height=30, bgcolor="#222222", border_radius=15),
            ft.Container(width=4, height=30, left=150, bgcolor="#888888"),  
            drift_dot
        ]),
        visible=False)
    

    button_width = 100
    action_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        controls=[
            ft.FilledButton("Calibrate", on_click=calibrate, width=button_width, style=ft.ButtonStyle(
                    overlay_color=ft.Colors.GREEN_100,             # hover background color
                    color=ft.Colors.GREEN_800,                     # text color
                    side=ft.BorderSide(width=1, color=ft.Colors.GREEN_600),  # border color
                        ),),
            ft.FilledTonalButton("▶ Start", on_click=start_tracking, width=button_width, style=ft.ButtonStyle(
                    overlay_color=ft.Colors.BLUE_100,             # hover background color
                    color=ft.Colors.BLUE_800,                     # text color
                    side=ft.BorderSide(width=1, color=ft.Colors.BLUE_50),  # border color
                        ),),
            ft.OutlinedButton("Stop", on_click=stop_tracking_btn, width=button_width, 
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.RED_100,             # hover background color
                    color=ft.Colors.RED_600,                     # text color
                    side=ft.BorderSide(width=1, color=ft.Colors.RED_600),  # border color
                        ),),
        ]
    )



    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            controls=[
                #C1
                ft.Container(
                    width=250,
                    padding=16,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=8,
                    content=instruction_text
                ),

                #C2
                ft.Container(
                    bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    width=360,
                    padding=16,
                    border_radius=8,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=18,
                        controls=[
                            title,
                            subtitle,
                            status,
                            action_buttons,
                            iris_position_text,
                            counter_balance,
                            lane_display,   
                            feedback,
                        ]
                    )
                ),

                #C3
                ft.Container(
                    width=260,
                    padding=16,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=8,
                    content=ft.Column([
                        drift_log_label,
                        drift_log
                    ])
                ),
            ]
        )
    )

ft.app(target=main)