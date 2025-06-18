import cv2
import os
import csv
import numpy as np
import pyttsx3
import speech_recognition as sr
from utils.speech_engine import speak  # Assuming your TTS function is here

# Paths
DATASET_DIR = "assets/known_faces"
MODEL_PATH = "models/model.yml"
CSV_PATH = os.path.join(DATASET_DIR, "people.csv")
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Setup
os.makedirs(DATASET_DIR, exist_ok=True)
engine = pyttsx3.init()
recognizer = sr.Recognizer()
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Load ID → name mapping
def load_people_csv():
    if not os.path.exists(CSV_PATH):
        return {}
    with open(CSV_PATH, mode='r', newline='') as f:
        reader = csv.reader(f)
        return {int(row[0]): row[1] for row in reader}

# Save new entry
def append_to_csv(person_id, name):
    with open(CSV_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([person_id, name])

# Train model from images
def train_model():
    print("Training model...")
    faces, ids = [], []
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith(".jpg"):
            try:
                path = os.path.join(DATASET_DIR, filename)
                parts = filename.split("-")
                name, count, person_id = parts[0], parts[1], parts[2].split('.')[0]
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    faces.append(img)
                    ids.append(int(person_id))
            except Exception as e:
                print("Skipped:", filename, e)
    if not faces:
        print("No data to train.")
        return
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.save(MODEL_PATH)
    print("Model trained and saved.")

# Ask for permission to save unknown face
def ask_to_save():
    speak("Do you want to save this unknown person?")
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
            response = recognizer.recognize_google(audio).lower()
            print("You said:", response)
            return "yes" in response
    except:
        response = input("Do you want to save this person? (yes/no): ").strip().lower()
        return response == "yes"

# Ask for name via voice (fallback to keyboard)
def ask_name():
    speak("What is their name?")
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
            name = recognizer.recognize_google(audio).strip()
            return name
    except:
        return input("Enter name: ").strip()

# Get next ID
def get_next_id(people_dict):
    return max(people_dict.keys(), default=0) + 1

# Save samples
def collect_samples(name, person_id):
    cam = cv2.VideoCapture(0)
    count = 0
    while count < 300:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            file_path = os.path.join(DATASET_DIR, f"{name}-{count}-{person_id}.jpg")
            cv2.imwrite(file_path, roi)
            count += 1
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f"{count}/300", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Saving new face", frame)
        if cv2.waitKey(1) == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    train_model()

# Main function
def run():
    people = load_people_csv()
    announced = set()

    if not os.path.exists(MODEL_PATH):
        speak("No trained model found.")
        if ask_to_save():
            name = ask_name()
            new_id = get_next_id(people)
            append_to_csv(new_id, name)
            collect_samples(name, new_id)
            people[new_id] = name
        else:
            speak("Okay, exiting.")
            return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    cap = cv2.VideoCapture(0)
    speak("Face detection started. Say stop face detection or scan new face to interact.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi)

            if confidence < 70 and label in people:
                name = people[label]
                if label not in announced:
                    speak(f"{name} is in front of you")
                    announced.add(label)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Face Detection", frame)

        # Voice command listener
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                command = recognizer.recognize_google(audio).lower()

                if "stop face detection" in command:
                    speak("Stopping face detection.")
                    break

                elif "scan new face" in command:
                    speak("Starting new face scan.")
                    name = ask_name()
                    new_id = get_next_id(people)
                    append_to_csv(new_id, name)
                    collect_samples(name, new_id)
                    people[new_id] = name
                    recognizer.read(MODEL_PATH)
                    announced.add(new_id)
        except:
            pass

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# For standalone testing
if __name__ == "__main__":
    run()
