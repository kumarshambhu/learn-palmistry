import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw
from scipy.special import comb

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

    def detect_hand_type(self, hand_landmarks):
        if not hand_landmarks:
            return "Hand not detected"

        # Using the first detected hand
        landmarks = hand_landmarks[0].landmark

        # Helper to calculate distance
        def _calculate_distance(p1, p2):
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

        # Palm width: Distance between the base of the index and pinky fingers
        palm_width = _calculate_distance(landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP],
                                         landmarks[self.mp_hands.HandLandmark.PINKY_MCP])

        # Palm height: Distance from the wrist to the base of the middle finger
        palm_height = _calculate_distance(landmarks[self.mp_hands.HandLandmark.WRIST],
                                          landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP])

        # Middle finger length: Distance from the base to the tip of the middle finger
        finger_length = _calculate_distance(landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                                            landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP])

        # Classification logic
        is_long_palm = palm_height > palm_width
        is_long_fingers = finger_length > palm_height

        if not is_long_palm and not is_long_fingers:
            return "Earth"
        elif not is_long_palm and is_long_fingers:
            return "Air"
        elif is_long_palm and is_long_fingers:
            return "Water"
        elif is_long_palm and not is_long_fingers:
            return "Fire"
        else:
            return "Could not determine hand type"

    def draw_palmistry_lines(self, pil_image, hand_landmarks):
        if not hand_landmarks:
            return pil_image

        image = pil_image.copy()
        draw = ImageDraw.Draw(image)
        width, height = image.size

        for landmarks in hand_landmarks:
            # Heart Line
            p1 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x * width, landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y * height])
            p2 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x * width, landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y * height])
            control = np.array([(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 30])
            points = np.array([p1, control, p2])
            x, y = self._bezier_curve(points, nTimes=20)
            draw.line(list(zip(x, y)), fill="red", width=2)

            # Head Line
            p1 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC].x * width, landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC].y * height])
            p2 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x * width, landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y * height])
            control = np.array([(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 10])
            points = np.array([p1, control, p2])
            x, y = self._bezier_curve(points, nTimes=20)
            draw.line(list(zip(x, y)), fill="blue", width=2)

            # Life Line
            p1 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC].x * width, landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC].y * height])
            p2 = np.array([landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * width, landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * height])
            control = np.array([p1[0] - 40, (p1[1] + p2[1]) / 2])
            points = np.array([p1, control, p2])
            x, y = self._bezier_curve(points, nTimes=20)
            draw.line(list(zip(x, y)), fill="green", width=2)

        return image

    def _bernstein_poly(self, i, n, t):
        return comb(n, i) * (t**(n-i)) * (1 - t)**i

    def _bezier_curve(self, points, nTimes=1000):
        nPoints = len(points)
        xPoints = np.array([p[0] for p in points])
        yPoints = np.array([p[1] for p in points])

        t = np.linspace(0.0, 1.0, nTimes)

        polynomial_array = np.array([self._bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

        xvals = np.dot(xPoints, polynomial_array)
        yvals = np.dot(yPoints, polynomial_array)

        return xvals, yvals