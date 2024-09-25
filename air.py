import cv2
import mediapipe as mp
import lirc

# Setup LIRC
sockid = lirc.init("myremote")  # "myremote" should match your LIRC configuration

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(0)
current_aircon_state = 'off'
mode = 'None'

def send_ir_command(command):
    lirc.send_once("myremote", command)  # Replace "myremote" with your remote name

def light_or_airCon(handLandmarks, handLabel):
    # (Same logic as before...)
    return ""

def turn_on_or_off(handLandmarks, handLabel):
    # (Same logic as before, but call send_ir_command)
    if (handLandmarks[8][1] < handLandmarks[6][1]):  # Example condition
        if current_aircon_state == 'off':
            send_ir_command("AC_ON")  # Use your actual command here
            return "turn on"
        else:
            send_ir_command("AC_OFF")  # Use your actual command here
            return "turn off"
    return ""

def adjust_airCon(handLandmarks):
    # (Adjust based on hand gestures, call send_ir_command)
    return ""

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while capture.isOpened():
        success, image = capture.read()
        if not success:
            print('Ignored empty webcam\'s frame')
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        outcome = ""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                handLabel = results.multi_handedness[handIndex].classification[0].label

                handLandmarks = []
                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])

                if mode == 'None':
                    outcome = light_or_airCon(handLandmarks, handLabel)
                    if outcome == "airCon":
                        mode = "airCon"

                elif mode == "airCon":
                    outcome = turn_on_or_off(handLandmarks, handLabel)
                    if outcome == "turn on":
                        current_aircon_state = 'on'
                    elif outcome == "turn off":
                        current_aircon_state = 'off'

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        cv2.imshow('Air Conditioner Control', image)
        if cv2.waitKey(100) == 27:  # Press ESC to exit
            break

capture.release()
lirc.deinit()
