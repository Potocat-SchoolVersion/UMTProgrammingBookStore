import os
import cv2 as cv
import time
import face_recognition

def draw_corner_rect(img, x, y, w, h, color, thickness=2, corner_frac=0.2):
    x2, y2 = x + w, y + h
    corner_len_w = int(w * corner_frac)
    corner_len_h = int(h * corner_frac)

    # Top-left
    cv.line(img, (x, y), (x + corner_len_w, y), color, thickness)
    cv.line(img, (x, y), (x, y + corner_len_h), color, thickness)

    # Top-right
    cv.line(img, (x2, y), (x2 - corner_len_w, y), color, thickness)
    cv.line(img, (x2, y), (x2, y + corner_len_h), color, thickness)

    # Bottom-left
    cv.line(img, (x, y2), (x + corner_len_w, y2), color, thickness)
    cv.line(img, (x, y2), (x, y2 - corner_len_h), color, thickness)

    # Bottom-right
    cv.line(img, (x2, y2), (x2 - corner_len_w, y2), color, thickness)
    cv.line(img, (x2, y2), (x2, y2 - corner_len_h), color, thickness)


def scan_and_capture_steady_face(
    cascade_path=None,
    camera_index=0,
    min_width=100,
    min_height=100,
    steady_seconds=1.0,
    position_thresh=20,
    area_change_thresh=0.15,
):
    cap = cv.VideoCapture(camera_index)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    if cascade_path is None:
        cascade_path = cv.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        print("Error: Could not load Haar cascade.")
        cap.release()
        return None

    red = (0, 0, 255)
    last_box = None
    steady_start_time = None
    captured = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Error: Failed to read frame from camera.")
                break

            frame_copied = frame.copy()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(min_width, min_height)
            )

            now = time.time()

            if len(faces) == 1:
                x, y, w, h = faces[0]
                current_box = (x, y, w, h)

                draw_corner_rect(frame, x, y, w, h, red, thickness=2, corner_frac=0.10)

                if last_box is None:
                    last_box = current_box
                    steady_start_time = now
                else:
                    lx, ly, lw, lh = last_box

                    cx, cy = x + w / 2, y + h / 2
                    lcx, lcy = lx + lw / 2, ly + lh / 2
                    dx = abs(cx - lcx)
                    dy = abs(cy - lcy)

                    area = w * h
                    last_area = lw * lh
                    area_change = abs(area - last_area) / last_area if last_area > 0 else 0

                    if dx <= position_thresh and dy <= position_thresh and area_change <= area_change_thresh:
                        if steady_start_time is None:
                            steady_start_time = now
                        # this line was useless: elapsed = now - steady_seconds
                        elapsed = now - steady_start_time

                        cv.putText(frame, f"Hold still: {elapsed:.1f}/{steady_seconds:.1f}s",
                                   (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, red, 1)

                        if elapsed >= steady_seconds:
                            # ---- CROP FACE HERE ----
                            h_img, w_img = frame_copied.shape[:2]
                            x1 = max(0, x)
                            y1 = max(0, y)
                            x2 = min(w_img, x + w)
                            y2 = min(h_img, y + h)

                            face_roi = frame_copied[y1:y2, x1:x2]
                            captured = face_roi
                            break
                    else:
                        steady_start_time = now

                    last_box = current_box

            else:
                last_box = None
                steady_start_time = None

            cv.imshow("Face Scanner", frame)

            if cv.waitKey(1) & 0xFF == ord("q"):
                print("Cancelled by user.")
                break

    finally:
        cap.release()
        cv.destroyAllWindows()

    return captured


def face_comparision(target_image_name, threshold=0.4):
    is_same = False
    distance = -1.0

    # find enrolled image
    image_folder = rf"{"\\".join(os.getcwd().split("\\"))}\data\faces"
    selected_path = rf""
    for image in os.listdir(image_folder):
        if image[:-4] == target_image_name:
            selected_path = rf"{image_folder}\{image}"
            break

    if not selected_path:
        print("No enrolled image found for this phone number.")
        return is_same, distance

    print("Selected:", selected_path)

    # load and encode enrolled face
    recognized_image = face_recognition.load_image_file(selected_path)
    recognized_encoding = face_recognition.face_encodings(recognized_image)
    if len(recognized_encoding) == 0:
        print("No face found in enrolled image.")
        return is_same, distance
    face1 = recognized_encoding[0]

    # capture live face
    captured = scan_and_capture_steady_face(steady_seconds=1.5)
    if captured is not None:
        # BGR -> RGB
        captured_rgb = cv.cvtColor(captured, cv.COLOR_BGR2RGB)
        unrecognized_encoding = face_recognition.face_encodings(captured_rgb)

        if len(unrecognized_encoding) == 0:
            print("No face found in captured image.")
            return is_same, distance

        face2 = unrecognized_encoding[0]

        distance = face_recognition.face_distance([face1], face2)[0]
        is_same = distance <= threshold

    return is_same, distance


# is_same, dist = face_comparision("601116181428")
# print(is_same, dist)
