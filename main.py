import cv2
import face_recognition
import pickle

# Load encodings
with open("encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)

    encodings = []
    if len(faces) > 0:
        encodings = face_recognition.face_encodings(rgb, faces)

    for encode_face, face_loc in zip(encodings, faces):
        matches = face_recognition.compare_faces(known_encodings, encode_face)

        name = "Unknown"
        if True in matches:
            index = matches.index(True)
            name = known_names[index]

        top, right, bottom, left = face_loc

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()