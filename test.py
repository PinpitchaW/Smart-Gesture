import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils #วาดจุดและเส้นบนมือที่จับได้
mp_drawing_styles = mp.solutions.drawing_styles #เปลี่ยนสไตล์การวาด
mp_hands = mp.solutions.hands #รับข้อมูลมือ

capture = cv2.VideoCapture(0) #กล้องที่ใช้ในการจับภาพคือกล้อง webcam(เลข0)
with mp_hands.Hands( #ข้อมูลมือ
  model_complexity=0, #ความซับซ้อนต่ำ
  min_detection_confidence=0.5, #ความมั่นใจขั้นต่ำในการตรวจจับมือ
  min_tracking_confidence=0.5) as hands: #ความมั่นใจขั้นต่ำในการติดตามมือ
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
    
    fingerCount = 0

    if results.multi_hand_landmarks: #ตำแหน่งของมือ 21 จุด คิดเป็นเปอร์เซ็นต์ของภาพ
      for hand_landmarks in results.multi_hand_landmarks: #วนในแต่ละมือที่จับได้
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label #มือซ้ายหรือขวา

        handLandmarks = [] #ตำแหน่งแต่ละจุดของมือ

        for landmarks in hand_landmarks.landmark: #เพิ่มตำแหน่งลงไป
          handLandmarks.append([landmarks.x, landmarks.y])
        
        #นิ้วโป้ง
        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]: #มือซ้าย ปลายนิ้วโป้งจะอยู่ทางขวาของข้อนิ้วโป้งในหน้ามือ
          fingerCount = fingerCount + 1
        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]: #มือซ้าย ปลายนิ้วโป้งจะอยู่ทางซ้ายของข้อนิ้วโป้งในหน้ามือ
          fingerCount = fingerCount + 1

        if handLandmarks[8][1] < handLandmarks[6][1]: #นิ้วชี้
          fingerCount = fingerCount + 1
        if handLandmarks[12][1] < handLandmarks[10][1]: #นิ้วกลาง
          fingerCount = fingerCount + 1
        if handLandmarks[16][1] < handLandmarks[14][1]: #นิ้วนาง
          fingerCount = fingerCount + 1
        if handLandmarks[20][1] < handLandmarks[18][1]: #นิ้วก้อย
          fingerCount = fingerCount + 1

        mp_drawing.draw_landmarks( #วาดจุดและเส้นบนมือ
          image, #ภาพจากกล้อง
          hand_landmarks, #จุด
          mp_hands.HAND_CONNECTIONS, #เส้น
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style()
        )

    cv2.putText(image, str(fingerCount), (50,450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,0,0), 10) #แสดงจำนวนนิ้วที่นับได้บนภาพ
    cv2.imshow('FingerCounting Apps',image) #แสดงผลสิ่งที่กล้องจับได้
    if cv2.waitKey(1) == 27: #กด ESC เพื่อออกจากโปรแกรม
        break
  capture.release() #ปิดกล้อง