import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Define constants and model setup
actions = np.array(["الحمدللة","الا القاء","مساءالنور","شكرا"])

colors = [(245,117,16), (117,245,16), (16,117,245), 
          (245,16,117), (117,16,245), (16,245,117),
          (245,245,16), (16,245,245), (245,16,245),
          (16,16,245), (245,16,16)]

# Initialize the Mediapipe holistic model and drawing utils
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Function to detect mediapipe landmarks
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

# Function to draw landmarks on the frame
def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

# Function to extract keypoints from the mediapipe results
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])

# Function to visualize probabilities
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    #for num, prob in enumerate(res):
       # cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num % len(colors)], -1)
        #cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    return output_frame

# Load the model
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(60,258)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(actions), activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

try:

    model.load_weights('D:\GraduationProjecGPmainproject\GraduationProject-main\project1\detection\model\Dynamic.h5')
    print("Loaded model from disk")
except Exception as e:
    print("Error loading model:", e)

class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.8
    
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            return None

        image, results = mediapipe_detection(frame, self.holistic)
        draw_styled_landmarks(image, results)

        keypoints = extract_keypoints(results)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-60:]

        if len(self.sequence) == 60:
            res = model.predict(np.expand_dims(self.sequence, axis=0))[0]
            self.predictions.append(np.argmax(res))

            if np.unique(self.predictions[-10:])[0] == np.argmax(res):
                if res[np.argmax(res)] > self.threshold:
                    if len(self.sentence) > 0:
                        if actions[np.argmax(res)] != self.sentence[-1]:
                            self.sentence.append(actions[np.argmax(res)])
                    else:
                        self.sentence.append(actions[np.argmax(res)])

            if len(self.sentence) > 5:
                self.sentence = self.sentence[-5:]

            image = prob_viz(res, actions, image, colors)

        #cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        #cv2.putText(image, ' '.join(self.sentence), (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        print(self.sentence)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), self.sentence if self.sentence else ""
