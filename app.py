import face_recognition
import numpy as np
from flask import Flask, render_template, Response, request, redirect, session
import cv2
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

stop_camera = False

# ================= LOAD DATASET =================
known_encodings = []
known_names = []

dataset_path = "dataset"

for file in os.listdir(dataset_path):
    img_path = os.path.join(dataset_path, file)
    img = face_recognition.load_image_file(img_path)

    encodings = face_recognition.face_encodings(img)

    if len(encodings) > 0:
        known_encodings.append(encodings[0])
        known_names.append(os.path.splitext(file)[0])


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "admin@1234":
            session['user'] = "admin"
            return redirect('/')
        return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ================= ATTENDANCE =================
def mark_attendance(name):
    file_path = "attendance.csv"
    today = datetime.now().strftime("%Y-%m-%d")

    # 🔥 Prevent duplicate for same day
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4 and row[0] == name and row[1] == today:
                    return

    now = datetime.now()

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            name,
            today,
            now.strftime("%H:%M:%S"),
            "Present"
        ])


def mark_absent(marked):
    file_path = "attendance.csv"
    today = datetime.now().strftime("%Y-%m-%d")

    all_students = set(known_names)
    absent_students = all_students - marked

    existing_today = set()

    # 🔥 Check already marked today
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2 and row[1] == today:
                    existing_today.add(row[0])

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        for name in absent_students:
            if name not in existing_today:
                writer.writerow([name, today, "-", "Absent"])


# ================= CAMERA =================
def generate_frames():
    global stop_camera
    stop_camera = False

    cap = cv2.VideoCapture(0)
    marked = set()

    while True:
        if stop_camera:
            break

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for encoding, location in zip(face_encodings, face_locations):

            distances = face_recognition.face_distance(known_encodings, encoding)

            if len(distances) == 0:
                continue

            index = np.argmin(distances)

            name = "Unknown"
            note = ""

            if distances[index] < 0.6:
                name = known_names[index]

                if name not in marked:
                    mark_attendance(name)
                    note = "Attendance Marked"
                    marked.add(name)
                else:
                    note = "Already Marked"

            # UI
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            top, right, bottom, left = location

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)

            cv2.putText(frame, name, (left + 5, bottom - 8),
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            if note:
                cv2.putText(frame, note, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    mark_absent(marked)


# ================= ROUTES =================
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('camera.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop')
def stop():
    global stop_camera
    stop_camera = True
    return "Stopped"


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    today = datetime.now().strftime("%Y-%m-%d")

    data = []
    present = 0
    absent = 0

    if os.path.exists("attendance.csv"):
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:

                if len(row) < 4:
                    continue

                # 🔥 ONLY TODAY DATA
                if row[1] != today:
                    continue

                data.append(row)

                if row[3] == "Present":
                    present += 1
                elif row[3] == "Absent":
                    absent += 1

    return render_template("dashboard.html",
                           data=data,
                           present=present,
                           absent=absent)


if __name__ == "__main__":
    app.run(debug=True)