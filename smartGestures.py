import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils #วาดจุดและเส้นบนมือที่จับได้
mp_drawing_styles = mp.solutions.drawing_styles #เปลี่ยนสไตล์การวาด
mp_hands = mp.solutions.hands #รับข้อมูลมือ

capture = cv2.VideoCapture(0) #กล้องที่ใช้ในการจับภาพคือกล้อง webcam(เลข0)

def light_or_airCon(handLandmarks, handLabel):
    #ตรวจสอบ นิ้วชี้ กลาง นาง ก้อย โป้ง ตามลำดับ
    #เมื่อชูนิ้วโป้ง มือซ้าย ปลายนิ้วโป้งจะอยู่ทางขวาของข้อนิ้วโป้งในหน้ามือ และมือขวา ปลายนิ้วโป้งจะอยู่ทางซ้ายของข้อนิ้วโป้งในหน้ามือ

    # 1 นิ้ว เลือกไฟ
    if (handLandmarks[8][1] < handLandmarks[6][1] and 
        handLandmarks[12][1] > handLandmarks[10][1] and 
        handLandmarks[16][1] > handLandmarks[14][1] and 
        handLandmarks[20][1] > handLandmarks[18][1] and 
        ((handLabel == "Left" and handLandmarks[4][0] < handLandmarks[3][0]) or 
        (handLabel == "Right" and handLandmarks[4][0] > handLandmarks[3][0]))):
        return("light")

    # 2 นิ้ว เพื่อเลือกเครื่องปรับอากาศ
    elif (handLandmarks[8][1] < handLandmarks[6][1] and 
          handLandmarks[12][1] < handLandmarks[10][1] and 
          handLandmarks[16][1] > handLandmarks[14][1] and 
          handLandmarks[20][1] > handLandmarks[18][1] and 
          ((handLabel == "Left" and handLandmarks[4][0] < handLandmarks[3][0]) or 
          (handLabel == "Right" and handLandmarks[4][0] > handLandmarks[3][0]))):
        return("airCon")
    return ""

def turn_on_or_off(handLandmarks, handLabel):
    # 5 นิ้ว เพื่อเลือกว่าจะเปิด
    if (handLandmarks[8][1] < handLandmarks[6][1] and 
          handLandmarks[12][1] < handLandmarks[10][1] and 
          handLandmarks[16][1] < handLandmarks[14][1] and 
          handLandmarks[20][1] < handLandmarks[18][1] and 
          handLandmarks[8][1] < handLandmarks[5][1] and 
          handLandmarks[12][1] < handLandmarks[9][1] and 
          handLandmarks[16][1] < handLandmarks[13][1] and 
          handLandmarks[20][1] < handLandmarks[17][1] and 
          handLandmarks[2][1] > handLandmarks[5][1] and 
          ((handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]) or 
          (handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]))):
        return("turn on")
    elif ((handLandmarks[0][1] > handLandmarks[2][1] and
            handLandmarks[8][1] > handLandmarks[6][1] and
            handLandmarks[12][1] > handLandmarks[10][1] and
            handLandmarks[16][1] > handLandmarks[14][1] and
            handLandmarks[20][1] > handLandmarks[18][1] and
            handLandmarks[4][1] < handLandmarks[8][1] and
            handLandmarks[3][1] > handLandmarks[6][1])):
          return("turn off")
    return("")

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
            # การเลื่อนขึ้นหรือลงดูจากการเปลี่ยนแปลงค่า Y ของนิ้วชี้และนิ้วโป้ง
            thumb_movement = thumb_tip[1] - prev_thumb_y
            index_movement = index_tip[1] - prev_index_y

            # ตรวจสอบว่าการเคลื่อนไหวคือเลื่อนขึ้นหรือลง
            if thumb_movement < -0.02 and index_movement < -0.02:
                return "increase", thumb_tip[1], index_tip[1]  # เลื่อนขึ้น
            elif thumb_movement > 0.02 and index_movement > 0.02:
                return "decrease", thumb_tip[1], index_tip[1]  # เลื่อนลง
            
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
      return("increase")
    if count == 6: 
      return("decrease")
    count = 0
    print("")
    return("")

def end_work(handLandmarks):
    if (handLandmarks[0][1] > handLandmarks[2][1] and
      handLandmarks[8][1] > handLandmarks[6][1] and
      handLandmarks[12][1] > handLandmarks[10][1] and
      handLandmarks[16][1] > handLandmarks[14][1] and
      handLandmarks[20][1] > handLandmarks[18][1] 
       ):
        return ("end")
    return("")

with mp_hands.Hands( #ข้อมูลมือ
  model_complexity=0, #ความซับซ้อนต่ำ
  min_detection_confidence=0.5, #ความมั่นใจขั้นต่ำในการตรวจจับมือ
  min_tracking_confidence=0.5) as hands: #ความมั่นใจขั้นต่ำในการติดตามมือ

  thumb_y = None
  index_y = None
  mode = None
  # light = "off"
  # airCon ="off"

  while capture.isOpened(): #เมื่อเปิดกล้อง
    success, image = capture.read() #รับรูปจาก webcam เพื่อสร้างเป็นวิดีโอ
    if not success: #ไม่มีภาพจากกล้อง
      print('Ignored empty webcam\'s frame')
      continue
    image.flags.writeable = False #ตั้งให้เป็น false เพื่อบอกว่าภาพจะไม่เปลี่ยนเมื่อประมวลผล ทำให้ทำงานเร็วขึ้นและใช้หน่วยความจำต่ำลง
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #กล้องได้สีแบบ BGR จึงเปลี่ยนให้เป็น RGB เพื่อใช้ร่วมกับ mediapipe
    results = hands.process(image) #ตรวจจับมือในภาพที่แปลงเป็น RGB แล้ว

    image.flags.writeable = True #ตั้งกลับเป็น true เพื่อวาดจุดและเส้นบนมือ
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    outcome = ""
    
    if results.multi_hand_landmarks: #ตำแหน่งของมือ 21 จุด คิดเป็นเปอร์เซ็นต์ของภาพ
      for hand_landmarks in results.multi_hand_landmarks: #วนในแต่ละมือที่จับได้
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label #มือซ้ายหรือขวา

        handLandmarks = [] #ตำแหน่งแต่ละจุดของมือ

        for landmarks in hand_landmarks.landmark: #เพิ่มตำแหน่งลงไป
          handLandmarks.append([landmarks.x, landmarks.y])

        if mode == None :
          # เลือกว่าจะควบคุมไฟหรือเครื่องปรับอากาศ
          outcome = light_or_airCon(handLandmarks, handLabel)
          if outcome == "light" :
            mode = "light"
          elif outcome == "airCon" :
            mode = "airCon"

        elif mode == "light" :
            # เลือกว่าจะเปิดหรือปิดไฟ
            outcome = turn_on_or_off(handLandmarks, handLabel)
            if outcome == "turn on" :
              mode = "light-on"
            elif outcome == "turn off" :
              print('turn off')

            outcome = end_work(handLandmarks)
            if outcome == "end" :
                mode = None

        elif mode == "airCon" :
            outcome = turn_on_or_off(handLandmarks, handLabel)
            if outcome == "turn on" :
              mode = "airCon-on"
            elif outcome == "turn off" :
              print('turn off')

            outcome = end_work(handLandmarks)
            if outcome == "end" :
                mode = None
      
        elif mode == "light-on" :
            outcome, thumb_y, index_y = adjust_light(handLandmarks, thumb_y, index_y)
            if outcome == "increase" :
              print('increase')
            elif outcome == "decrease" :
              print('decrease')

            outcome = end_work(handLandmarks)
            if outcome == "end" :
                mode = None

        elif mode == "airCon-on" :
            outcome = adjust_airCon(handLandmarks)
            if outcome == "increase" :
              print('increase')
            elif outcome == "decrease" :
              print('decrease')

            outcome = end_work(handLandmarks)
            if outcome == "end" :
                mode = None  
        # # เลือกว่าจะควบคุมไฟหรือเครื่องปรับอากาศ
        # outcome = light_or_airCon(handLandmarks, handLabel)
        # if outcome == "" :
        #   outcome = turn_on_or_off(handLandmarks, handLabel)
        #   if outcome == "" :
        #       outcome, thumb_y, index_y = adjust_light(handLandmarks, thumb_y, index_y)
        #       if outcome == "" :
        #           # thumb_y = None
        #           # index_y = None
        #           outcome = adjust_airCon(handLandmarks)
        #           if outcome == "" :
        #             outcome = end_work(handLandmarks)

        mp_drawing.draw_landmarks( #วาดจุดและเส้นบนมือ
          image, #ภาพจากกล้อง
          hand_landmarks, #จุด
          mp_hands.HAND_CONNECTIONS, #เส้น
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style()
        )

    cv2.putText(image, str(outcome), (50,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,0,0), 10) #แสดงจำนวนนิ้วที่นับได้บนภาพ
    cv2.imshow('outcomeing Apps',image) #แสดงผลสิ่งที่กล้องจับได้
    if cv2.waitKey(100) == 27: #กด ESC เพื่อออกจากโปรแกรม
        break
  capture.release() #ปิดกล้อง