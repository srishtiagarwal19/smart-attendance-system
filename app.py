import face_recognition
import numpy as np
from flask import Flask, render_template, Response, redirect, url_for, request, session
import cv2
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- LOAD DATASET ----------------
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

# ---------------- MARK ATTENDANCE ----------------
def mark_attendance(name):
    file_path = "attendance.csv"
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Prevent duplicate for same session
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time, "Present"])

# ---------------- CAMERA ----------------
def generate_frames():
    cap = cv2.VideoCapture(0)
    marked = set()

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            if len(face_distances) == 0:
                continue

            best_match_index = np.argmin(face_distances)

            name = "Unknown"

            if face_distances[best_match_index] < 0.5:
                name = known_names[best_match_index]

                if name not in marked:
                    mark_attendance(name)
                    marked.add(name)

            top, right, bottom, left = face_location

            # Green for known, Red for unknown
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "admin@1234":
            session['user'] = "admin"
            return redirect('/')
        return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------------- HOME ----------------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

# ---------------- START CAMERA ----------------
@app.route('/start')
def start():
    return render_template('camera.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ---------------- STOP (UPDATED ✅) ----------------
@app.route('/stop')
def stop():
    return redirect(url_for('index'))   # 🔥 FIXED

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    data = []
    present_count = 0

    try:
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 4:
                    continue
                data.append(row)
                if row[3] == "Present":
                    present_count += 1
    except:
        pass

    total_people = len(known_names)
    absent_count = total_people - present_count

    return render_template("dashboard.html",
                           data=data,
                           present=present_count,
                           absent=absent_count,
                           total=total_people)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)