import cv2
import time
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
left_eye_points = list(range(36, 42))
right_eye_points = list(range(42, 48))

def get_eye_center(points, landmarks):
    coordinates = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
    return coordinates.mean(axis=0)

def is_looking_down(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye_center = get_eye_center(left_eye_points, landmarks)
        right_eye_center = get_eye_center(right_eye_points, landmarks)
        slope = (right_eye_center[1] - left_eye_center[1]) / (right_eye_center[0] - left_eye_center[0])
        if slope < 0:
            return True

    return False

def is_head_down(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        if landmarks.part(8).y - landmarks.part(27).y > 10:
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
        looking_down = is_looking_down(frame)
        if looking_down:
            if start_time is None:
                start_time = time.time()
            else:
                duration = time.time() - start_time
                if duration >= 30:
                    print("Looking down for 30 seconds")
        else:
            start_time = None
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()