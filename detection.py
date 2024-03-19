import os
import sys
import cv2
import time
import dlib
import numpy as np
from login import user_login_register
from aws.dynamodb import increment_phone_usage

if getattr(sys, 'frozen', False):
    dat_file = os.path.join(sys._MEIPASS, 'shape_predictor_68_face_landmarks.dat')
else:
    dat_file = 'shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dat_file)
left_eye_points = list(range(36, 42))
right_eye_points = list(range(42, 48))

def get_eye_center(points, landmarks):
    coordinates = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
    if len(coordinates) < 6:  
        return None
    return coordinates.mean(axis=0)


def capture_baseline(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if faces:
        face = faces[0]  
        landmarks = predictor(gray, face)
        left_eye_center = get_eye_center(left_eye_points, landmarks)
        right_eye_center = get_eye_center(right_eye_points, landmarks)
        chin = (landmarks.part(8).x, landmarks.part(8).y) 
        forehead = ((landmarks.part(19).x + landmarks.part(24).x) // 2, (landmarks.part(19).y + landmarks.part(24).y) // 2) 
        baseline_data = {
            'left_eye_center': left_eye_center,
            'right_eye_center': right_eye_center,
            'chin': chin,
            'forehead': forehead,
        }
        print(baseline_data)
        return baseline_data 
    return None  

def is_looking_down_baseline(baseline_data, frame):
    if baseline_data is None:
        return False
    left_eye_center_base = baseline_data['left_eye_center']
    right_eye_center_base = baseline_data['right_eye_center']
    chin_base = baseline_data['chin']
    forehead_base = baseline_data['forehead']
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces =  detector(gray)
    if len(faces) == 0 and chin_base[1] != None:
        return True
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye_center = get_eye_center(left_eye_points, landmarks)
        right_eye_center = get_eye_center(right_eye_points, landmarks)
        chin_center = landmarks.part(8).y
        forehead_center =  ((landmarks.part(19).y + landmarks.part(24).y) // 2)
        if(chin_center - chin_base[1] > 33 or forehead_center - forehead_base[1] > 33):
            return True
        if left_eye_center[1] - left_eye_center_base[1] > 33 or right_eye_center[1] - right_eye_center_base[1] > 33:
            return True
        if (landmarks == None):
            return True
    return False
        

def sens_setting(sens):
    global sensitivity
    sensitivity = sens
    


def main():
    user= user_login_register()
    cap = cv2.VideoCapture(0)
    start_time = None
    onPhone = 0
    cv2.namedWindow('Frame')
    cv2.resizeWindow('Frame', 600, 600)
    cv2.createTrackbar("Adjust sensitivity of phone detection (0-100)",'Frame', 0, 10, sens_setting)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            baseline_data = capture_baseline(frame)
            if baseline_data is not None:
                print("Baseline posture saved successfully.")
                cv2.destroyWindow('Frame')
                break  
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return  
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, "Press 'q' to quit", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if not ret:
            break
        computational = is_looking_down_baseline(baseline_data, frame)
        if computational:
            if start_time is None:
                start_time = time.time()
                continue
            if start_time is not None:
                duration = time.time() - start_time
                print(duration)
                if duration >= 5:
                    print("staring at phone for 15 seconds")
                    if user is not None:
                        increment_phone_usage(user)
                    start_time = None
        else:
            start_time = None
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
