# SMART SYSTEM CAPSTONE DESIGN
` 스마트 RC카 ` _ openCV를 이용한 감정인식과 각종 센서를 이용한 스마트 RC카
1. openCV를 이용한 얼굴 인식 기능
2. 장애물 감지 기능
3. 버튼과 I2C 인터페이스를 이용한 의사소통 기능
4. 미세먼지에 따른 창문 조절 기능

## Arduino

### 🌈 RCCar.ino
* RC카를 구동 시키는 파일

### 🌈 mise_window.ino
* 미세먼지가 일정 농도 이상이 되면 서보모터를 작동해 자동으로 창문을 닫는 기능 
(LCD 디스플레이 기능은 부가적)
* 압력센서로 압력을 입력받아 일정 압력 이상일 때 서보모터를 이용해 창문을 여는 기능

<hr>

## RaspberryPi

### 🌈 ultra_lcd.py
* 초음파 센서를 이용하여 장애물과의 거리가 일정 거리 이하로 가까워 졌을 때, 피에조 부저를 울려 경고음을 울려주는 기능
* 스위치를 이용하여 버튼을 눌렀을 때, 일정 시간동안 주어진 문구를 LCD 디스플레이에 보여주는 기능 (Good Day -> Thank you)

### 🌈 01_face_dataset.py
* count 수 만큼 카메라를 이용해 사용자의 얼굴을 RGB -> gray 스케일로 저장하는 작업

### 🌈 02_face_training.py
* 01 에서 저장된 이미지를 가지고 학습된 파일을 .yml로 저장하는 작업

### 🌈 03_face_recigniition.py
* 실시간 얼굴 인식을 통해 등록된(학습된) 사용자를 판별

  `😎 등록된 사용자일 때 :`   
  * id 값에 따른 등록된 사용자 이름을 디스플레이  
  * 5개의 LED가 반짝반짝 빛남  
  * 파에조 부저로 welcome 부저를 출력
  
  `😓 등록되지 않은 사용자일 때 :`  
  * 사용자 이름을 판별할수 없으므로 unknown 디스플레이  
  * 5개의 LED 중 RED LED만 출력  
  * 파에조 부저로 unwelcome 부저 출력  

### 🌈 faceSmileEyeDetection.py
* 얼굴과 눈, 미소를 인식하는 파일
