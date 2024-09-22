import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Initialize counts
light = 0
turn_on = 0
turn_off = 0
ac = 0
end = 0

# Start timer
start_time = time.time()
count_duration = 3  # Count for 3 seconds

capture = cv2.VideoCapture(0)

def light_or_airCon(handLandmarks, handLabel):
    if (handLandmarks[8][1] < handLandmarks[6][1] and 
        handLandmarks[12][1] > handLandmarks[10][1] and 
        handLandmarks[16][1] > handLandmarks[14][1] and 
        handLandmarks[20][1] > handLandmarks[18][1] and 
        ((handLabel == "Left" and handLandmarks[4][0] < handLandmarks[3][0]) or 
         (handLabel == "Right" and handLandmarks[4][0] > handLandmarks[3][0]))):
        return "light"

    elif (handLandmarks[8][1] < handLandmarks[6][1] and 
          handLandmarks[12][1] < handLandmarks[10][1] and 
          handLandmarks[16][1] > handLandmarks[14][1] and 
          handLandmarks[20][1] > handLandmarks[18][1] and 
          ((handLabel == "Left" and handLandmarks[4][0] < handLandmarks[3][0]) or 
           (handLabel == "Right" and handLandmarks[4][0] > handLandmarks[3][0]))):
        return "airCon"
    return ""

def turn_on_or_off(handLandmarks, handLabel):
    if (handLandmarks[8][1] < handLandmarks[6][1] and 
          handLandmarks[12][1] < handLandmarks[10][1] and 
          handLandmarks[16][1] < handLandmarks[14][1] and 
          handLandmarks[20][1] < handLandmarks[18][1] and 
          handLandmarks[8][1] < handLandmarks[5][1] and 
          handLandmarks[12][1] < handLandmarks[9][1] and 
          handLandmarks[16][1] < handLandmarks[13][1] and 
          handLandmarks[20][1] < handLandmarks[17][1] and 
          handLandmarks[2][1] > handLandmarks[5][1] and 
          handLandmarks[8][1] < handLandmarks[11][1] and 
          ((handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]) or 
           (handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]))):
        return "turn on"
    
    elif ((handLandmarks[0][1] > handLandmarks[2][1] and
            handLandmarks[8][1] > handLandmarks[6][1] and
            handLandmarks[12][1] > handLandmarks[10][1] and
            handLandmarks[16][1] > handLandmarks[14][1] and
            handLandmarks[20][1] > handLandmarks[18][1] and
            handLandmarks[4][1] < handLandmarks[8][1] and
            handLandmarks[3][1] > handLandmarks[6][1])):
        return "turn off"
    
    return ""

def adjust_light(handLandmarks, prev_thumb_y=None, prev_index_y=None):
    thumb_tip = handLandmarks[4]
    index_tip = handLandmarks[8]
    thumb_base = handLandmarks[2]
    index_base = handLandmarks[5]

    thumb_index_distance = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
    thumb_base_index_distance = ((thumb_base[0] - index_base[0]) ** 2 + (thumb_base[1] - index_base[1]) ** 2) ** 0.5
    
    if (thumb_index_distance < 0.05 and 
        thumb_base_index_distance < 0.2 and
        handLandmarks[12][1] < handLandmarks[10][1] and
        handLandmarks[16][1] < handLandmarks[14][1] and
        handLandmarks[20][1] < handLandmarks[18][1] and
        handLandmarks[12][1] < handLandmarks[9][1] and 
        handLandmarks[16][1] < handLandmarks[13][1] and 
        handLandmarks[20][1] < handLandmarks[17][1] and
        handLandmarks[2][1] > handLandmarks[5][1] ):

        if prev_thumb_y is not None and prev_index_y is not None:
            thumb_movement = thumb_tip[1] - prev_thumb_y
            index_movement = index_tip[1] - prev_index_y
            
            if thumb_movement < -0.02 and index_movement < -0.02:
                return "increase", thumb_tip[1], index_tip[1]
            elif thumb_movement > 0.02 and index_movement > 0.02:
                return "decrease", thumb_tip[1], index_tip[1]
            
        return "adjust light", thumb_tip[1], index_tip[1]
    return ("", thumb_tip[1], index_tip[1])

def adjust_airCon(handLandmarks):
    count = 0
    if ((handLandmarks[6][1] < handLandmarks[5][1]) and 
        (handLandmarks[6][1] < handLandmarks[9][1]) and 
        (handLandmarks[6][1] < handLandmarks[13][1]) and 
        (handLandmarks[6][1] < handLandmarks[17][1]) and
        (handLandmarks[8][1] < handLandmarks[10][1])):
        count += 2
    if (handLandmarks[4][1] < handLandmarks[5][1]):
        count += 2
    if ((handLandmarks[6][1] > handLandmarks[5][1]) and 
        (handLandmarks[6][1] > handLandmarks[9][1]) and 
        (handLandmarks[6][1] > handLandmarks[13][1]) and 
        (handLandmarks[6][1] > handLandmarks[17][1])):
        count += 3
    if (handLandmarks[4][1] > handLandmarks[5][1]):
        count += 3
    if count == 4: 
        return "increase"
    if count == 6: 
        return "decrease"
    
    return ""

def end_work(handLandmarks):
    if (handLandmarks[0][1] > handLandmarks[2][1] and
      handLandmarks[8][1] > handLandmarks[6][1] and
      handLandmarks[12][1] > handLandmarks[10][1] and
      handLandmarks[16][1] > handLandmarks[14][1] and
      handLandmarks[20][1] > handLandmarks[18][1]):
        return "end"
    return ""

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    mode = 'None'
    final_outcome = ""
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
                    if outcome == "light":
                        mode = "light"
                    elif outcome == "airCon":
                        mode = "airCon"

                elif mode == "light":
                    outcome = turn_on_or_off(handLandmarks, handLabel)
                    if outcome == "turn on":
                        mode = "light-on"
                    elif outcome == "turn off":
                        outcome = end_work(handLandmarks)
                        if outcome == "end":
                            mode = 'None'

                elif mode == "airCon":
                    outcome = adjust_airCon(handLandmarks)
                    if outcome == "increase":
                        ac += 1
                    elif outcome == "decrease":
                        ac -= 1
                
                # Draw hand landmarks
                mp_drawing.draw_landmarks(image, hand_landmarks,
                                           mp_hands.HAND_CONNECTIONS,
                                           mp_drawing_styles.get_default_hand_landmarks_style(),
                                           mp_drawing_styles.get_default_hand_connections_style())

                # Counting logic
                if outcome:
                    if outcome == "airCon":
                        ac += 1
                    elif outcome == "light":
                        light += 1
                    elif outcome == "turn on":
                        turn_on += 1
                    elif outcome == "turn off":
                        turn_off += 1
                    elif outcome == "end":
                        end += 1

        # Check if 3 seconds have passed
        if time.time() - start_time >= count_duration:
            # Get the final outcome based on counts
            outcome_counts = {
                "light": light,
                "airCon": ac,
                "turn_on": turn_on,
                "turn_off": turn_off,
                "end": end,
            }
            final_outcome = max(outcome_counts, key=outcome_counts.get)
            print("Final Outcome:", final_outcome)

            # Reset counts and timer
            light = 0
            ac = 0
            turn_on = 0
            turn_off = 0
            end = 0
            start_time = time.time()

        # Display results
        cv2.putText(image, str(mode + ' ' + final_outcome), (50, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
        cv2.imshow('outcoming Apps', image)
        if cv2.waitKey(100) == 27:  # Press ESC to exit
            break

capture.release()
cv2.destroyAllWindows()
