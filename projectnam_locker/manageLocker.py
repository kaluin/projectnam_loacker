import threading
import time
import RPi.GPIO as GPIO
from restApi import send_api
        
MAX = 4
sensorState= { 1:{'motorPin':2, 'magneticPin':3,  'magneticState':0, 'lockerState':0, 'noticeIllegalOpen':0},
               2:{'motorPin':4, 'magneticPin':17, 'magneticState':0, 'lockerState':0, 'noticeIllegalOpen':0},
               3:{'motorPin':14,'magneticPin':15, 'magneticState':0, 'lockerState':0, 'noticeIllegalOpen':0},
               4:{'motorPin':18,'magneticPin':23, 'magneticState':0, 'lockerState':0, 'noticeIllegalOpen':0}}        
        
GPIO_3V = [19,20,21,26]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for i in range(1,5):
    GPIO.setup(GPIO_3V[i-1], GPIO.OUT)
    GPIO.output(GPIO_3V[i-1], GPIO.HIGH)
    GPIO.setup(sensorState[i]['motorPin'], GPIO.OUT)
    GPIO.setup(sensorState[i]['magneticPin'], GPIO.IN)

def servoMotor(degree,t,pin):
    pwm=GPIO.PWM(pin, 50)
    pwm.start(4)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(degree)
    time.sleep(t)  
    pwm.stop()

for i in range(1,5):
    servoMotor(4, 0.2, sensorState[i]['motorPin'])
    
def servoMotorStart(pin):
    servoMotor(9,1,sensorState[pin]['motorPin'])
    sensorState[pin]['lockerState'] = 25
    sensorState[pin]['noticeIllegalOpen'] = 0

def neverOpenNotClosed(pin):
    sensorState[pin]['lockerState'] = -1
    
def manageLockerState():
    while True:
        for i in range(1,MAX+1):
            sensorState[i]['magneticState']=GPIO.input(sensorState[i]['magneticPin'])
            # status 1: 열림(끊김)  status 0: 닫힘(연결) 초기값 25
            if sensorState[i]['lockerState'] == 0 and sensorState[i]['magneticState'] ==1:
                if sensorState[i]['noticeIllegalOpen'] == 0:
                    print(i , "번 사물함 도난발생 도난발생 지금 즉시 사물함을 확인해주세")
                    senddata={"lockernum":i,"lockername":None,"otp":None}
                    response=send_api("/locker/illegal_open_detected", "POST", senddata)
                    if response is not None:
                        if response['result'] == "success":
                            print("도난 보고 성공")
                        elif response['result'] == "failed":
                            print("도난 보고 실패")
                    else:
                        print("도난 관련 값이 안넘어오네?")
                    sensorState[i]['noticeIllegalOpen'] = 1
            elif sensorState[i]['lockerState'] != 0:
                if sensorState[i]['magneticState'] == 1:
                    sensorState[i]['lockerState'] = 1
                elif sensorState[i]['magneticState'] == 0 and sensorState[i]['lockerState'] < 5 and sensorState[i]['lockerState'] >= 1:
                    sensorState[i]['lockerState']+=1
                elif sensorState[i]['lockerState'] > 5:
                    sensorState[i]['lockerState']-=1
            if sensorState[i]['lockerState'] == 5:
                sensorState[i]['lockerState'] = 0
                servoMotor(4,1,sensorState[i]['motorPin'])
                sensorState[i]['noticeIllegalOpen'] = 0
        time.sleep(0.5)
    for i in range(4):        
        GPIO.cleanup(GPIO_3V[i])
        GPIO.cleanup(sensorState[i]['motorPin'])
        GPIO.cleanup(sensorState[i]['magneticPin'])

thread = threading.Thread(target = manageLockerState)
thread.daemon = True
thread.start()

