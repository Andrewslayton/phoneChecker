import os
import sys
import cv2
import time
import dlib
import numpy as np

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
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye_center = get_eye_center(left_eye_points, landmarks)
        right_eye_center = get_eye_center(right_eye_points, landmarks)
        chin_center = landmarks.part(8).y
        forehead_center =  ((landmarks.part(19).y + landmarks.part(24).y) // 2)
        if( chin_base[1] - chin_center > 33 or forehead_base[1] - forehead_center > 33):
            return True
        if (chin_base[1] and not chin_center):
            return True
        if (forehead_base[1] and not forehead_center):
            return True
        

def is_looking_down(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye_center = get_eye_center(left_eye_points, landmarks)
        right_eye_center = get_eye_center(right_eye_points, landmarks)
        cv2.rectangle(frame, (int(left_eye_center[0]-5), int(left_eye_center[1]-5)), (int(left_eye_center[0]+5), int(left_eye_center[1]+5)), (0,255,0), 1)
        cv2.rectangle(frame, (int(right_eye_center[0]-5), int(right_eye_center[1]-5)), (int(right_eye_center[0]+5), int(right_eye_center[1]+5)), (0,255,0), 1)
        left_eye_top = min(landmarks.part(i).y for i in left_eye_points)
        right_eye_top = min(landmarks.part(i).y for i in right_eye_points)
        left_eye_bottom = max(landmarks.part(i).y for i in left_eye_points)
        right_eye_bottom = max(landmarks.part(i).y for i in right_eye_points)
        

    return False

def is_head_down(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        chin_center = (landmarks.part(8).x, landmarks.part(8).y)
        forehead_center = ((landmarks.part(19).x + landmarks.part(24).x) // 2, 
                           (landmarks.part(19).y + landmarks.part(24).y) // 2)
        cv2.circle(frame, chin_center, 5, (255, 0, 0), -1)
        cv2.circle(frame, forehead_center, 5, (255, 0, 0), -1)
        if chin_center[1] - forehead_center[1] < 50:  
            return True
    return False


def main():
    cap = cv2.VideoCapture(0)
    start_time = None
    onPhone = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Frame', frame)
        cv2.putText(frame, "Press 's' to save baseline posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            baseline_data = capture_baseline(frame)
            if baseline_data is not None:
                print("Baseline posture saved successfully.")
                break  
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return  
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        computational = is_looking_down_baseline(baseline_data, frame)
        looking_down = is_looking_down(frame)
        head_down = is_head_down(frame) 
        if computational:
            if start_time is None:
                start_time = time.time()
            else:
                duration = time.time() - start_time
                if duration >= 2:
                    print("stupid!! for 2 seconds")
        # if head_down:
        #     if start_time is None:
        #         start_time = time.time()
        #     else:
        #         duration = time.time() - start_time
        #         if duration >= 2:
        #             print("Head down for 2 seconds")
        # if looking_down:
        #     if start_time is None:
        #         start_time = time.time()
        #     else:
        #         duration = time.time() - start_time
        #         if duration >= 2:
        #             print("Looking down for 2 seconds")
        else:
            start_time = None
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
