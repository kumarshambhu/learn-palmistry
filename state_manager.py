class StateManager:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.photo1 = None
        self.photo2 = None
        self.hand_landmarks = None
        self.handedness = None
        self.gestures = None

    def _reset_state(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.hand_landmarks = None
        self.handedness = None
        self.gestures = None
