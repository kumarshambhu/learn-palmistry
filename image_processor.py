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
        return results.multi_hand_landmarks

    def draw_hand_landmarks(self, pil_image, hand_landmarks):
        if not hand_landmarks:
            return pil_image

        image_np = np.array(pil_image)
        if image_np.ndim == 2:  # Grayscale image
            annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        else:  # Color image
            annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        for landmarks in hand_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_image_np,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS)

        return Image.fromarray(cv2.cvtColor(annotated_image_np, cv2.COLOR_BGR2RGB))

    def _calculate_distance(self, landmark1, landmark2):
        return np.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)

    def classify_hand_type(self, hand_landmarks):
        if not hand_landmarks:
            return "Uncertain"

        # Get landmarks
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_FINGER_MCP]

        # Calculate distances
        palm_length = self._calculate_distance(wrist, middle_mcp)
        palm_width = self._calculate_distance(index_mcp, pinky_mcp)
        finger_length = self._calculate_distance(middle_mcp, middle_tip)

        if palm_length == 0 or palm_width == 0:
            return "Uncertain"

        # Classify based on ratios
        palm_ratio = palm_width / palm_length
        finger_to_palm_ratio = finger_length / palm_length

        if palm_ratio > 0.9:  # Square palm
            if finger_to_palm_ratio > 1.0:
                return "Air"
            else:
                return "Earth"
        else:  # Rectangular palm
            if finger_to_palm_ratio > 1.0:
                return "Water"
            else:
                return "Fire"

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