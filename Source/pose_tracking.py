import cv2
import mediapipe as mp
from settings import *
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_poses = mp.solutions.pose



class PoseTracking:
    def __init__(self):
        self.pose_tracking = mp_poses.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.feet_x = 0
        self.feet_y = 0
        self.results = None
        self.pose_closed = False


    def scan_feets(self, image):
        rows, cols, _ = image.shape

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.results = self.pose_tracking.process(image)

        # Draw the pose annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.feet_closed = False

        if self.results.pose_landmarks:
            x, y = self.results.pose_landmarks.landmark[30].x, self.results.pose_landmarks.landmark[30].y
            x1, y1 = self.results.pose_landmarks.landmark[29].x, self.results.pose_landmarks.landmark[29].y

            self.feet_x = int(((x+x1)/2) * SCREEN_WIDTH)
            self.feet_y = int(((y+y1)/2) * SCREEN_HEIGHT)

            mp_drawing.draw_landmarks(
                image,
                self.results.pose_landmarks,
                mp_poses.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        return image

    def get_feet_center(self):
        return (self.feet_x, self.feet_y)


    def display_feet(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)

    def is_feet_closed(self):

        pass


