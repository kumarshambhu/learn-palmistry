import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize MediaPipe Selfie Segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def detect_hands(self, pil_image):
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        results = self.hands.process(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
        return results.multi_hand_landmarks, results.multi_handedness

    def get_hand_gesture(self, hand_landmarks):
        if not hand_landmarks:
            return "Unknown"

        landmarks = hand_landmarks.landmark

        # Simple check for fist: are fingertips lower than pip joints?
        is_fist = (
            landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[self.mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.PINKY_TIP].y > landmarks[self.mp_hands.HandLandmark.PINKY_PIP].y
        )

        # Simple check for open palm: are fingertips higher than pip joints?
        is_open_palm = (
            landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP].y < landmarks[self.mp_hands.HandLandmark.RING_FINGER_PIP].y and
            landmarks[self.mp_hands.HandLandmark.PINKY_TIP].y < landmarks[self.mp_hands.HandLandmark.PINKY_PIP].y
        )

        if is_fist:
            return "Fist"
        elif is_open_palm:
            return "Open Palm"
        else:
            return "Unknown"

    def draw_hand_landmarks(self, pil_image, hand_landmarks, handedness, gestures):
        if not hand_landmarks:
            return pil_image

        image_np = np.array(pil_image)
        if image_np.ndim == 2:  # Grayscale image
            annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        else:  # Color image
            annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        for i, landmarks in enumerate(hand_landmarks):
            self.mp_drawing.draw_landmarks(
                annotated_image_np,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS)

            # Get hand type and gesture
            hand_type = handedness[i].classification[0].label
            gesture = gestures[i]

            # Get position for the text
            x = int(landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * image_np.shape[1])
            y = int(landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * image_np.shape[0])

            # Put text on the image
            cv2.putText(annotated_image_np, f"{hand_type} Hand: {gesture}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        return Image.fromarray(cv2.cvtColor(annotated_image_np, cv2.COLOR_BGR2RGB))

    def remove_background(self, pil_image):
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 20, 80], dtype="uint8")
        upper = np.array([50, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        b, g, r = cv2.split(result)
        filter = g.copy()
        ret, mask = cv2.threshold(filter, 10, 255, 1)
        img[mask == 255] = 255

        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def convert_to_grayscale(self, pil_image):
        return pil_image.convert('L')