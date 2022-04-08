import cv2
import mediapipe as mp
import numpy as np
import argparse
import sys
from streamlit_webrtc import webrtc_streamer
import av

NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32

def calculate_angle(a,b,c):
    x=np.array(c)-np.array(b)
    y=np.array(a)-np.array(b)

    l_x=np.sqrt(x.dot(x))
    l_y=np.sqrt(y.dot(y))

    dian=x.dot(y)

    cos_=dian/(l_x*l_y)

    angle_hu=np.arccos(cos_)

    angle_d=angle_hu*180/np.pi
        
    return angle_d 

# Get coordinates
def get_angle(part1,part2,part3,landmarks):

    point_a = [landmarks[part1].x,landmarks[part1].y,landmarks[part1].z]

    point_b = [landmarks[part2].x,landmarks[part2].y,landmarks[part2].z]

    point_c = [landmarks[part3].x,landmarks[part3].y,landmarks[part3].z]
    return calculate_angle(point_a, point_b, point_c)

def FitCondition(points,thr_vis,landmarks):
    points=np.array(points)
    for i in points:
        if(landmarks[i].visibility<thr_vis):
            return False
    return True


class VideoProcessor:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

        # Curl counter variables
        self.counter = 0 
        self.stage = None
    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        # Extract landmarks
        results = self.pose.process(image)
        try:
            landmarks = results.pose_world_landmarks.landmark

            skeleton_is_vis=FitCondition((LEFT_HIP, LEFT_KNEE, LEFT_ANKLE,RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE), 0.2,landmarks)
            if(skeleton_is_vis):
                # 1.squat count
                angle_l = get_angle(LEFT_HIP, LEFT_KNEE, LEFT_ANKLE,landmarks)
                angle_r = get_angle(RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE,landmarks)
                # Visualize angle
                cv2.putText(image, str(angle_l), 
                                (150,150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)

                ptStart = (150, 600)
                ptEnd = (150,int(880-angle_l*4))
                point_color = (0, 255, 0)  # BGR
                thickness = 6
                lineType = 4
                cv2.line(image, ptStart, ptEnd, point_color, thickness, lineType)

                # Curl counter logic
                if angle_l < 100 and angle_r < 100 \
                and landmarks[LEFT_KNEE].y<landmarks[LEFT_ANKLE].y:
                    self.stage = "down"
                if angle_l > 160 and angle_r > 160 and self.stage =='down'\
                and landmarks[LEFT_HIP].y<landmarks[LEFT_KNEE].y:
                    self.stage="up"
                    self.counter +=1
                    # print(counter)
            else:
                cv2.putText(image, "Please adjust the position", 
                            (180,50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        except:
            cv2.putText(image, "not skeleton", 
                            (300,50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # 2.
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (150,73), (245,117,16), -1)
        
        # Rep data
        # cv2.putText(image, 'REPS', (15,12), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        # cv2.putText(image, 'STAGE', (65,12), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        # cv2.putText(image, stage, 
        #             (60,60), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )               

        return av.VideoFrame.from_ndarray(image, format="bgr24")
webrtc_streamer(key="example", video_processor_factory=VideoProcessor,sendback_audio=False)
