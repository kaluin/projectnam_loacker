from tkinter import Tk, StringVar, Button, Entry, INSERT, Label , Canvas
from functools import partial
from messageBox import *
import canUsed
from restApi import send_api
from componentColor import *
import manageLocker
response=None
userName = ''
def add_Enter(window,display_text):
    global response
    inputOTP = display_text.get()
    
    senddata={"id":None,"lockername":None,"otp":None, "clientotp":inputOTP}
    response=send_api("/locker/verify_OTP", "POST", senddata)
    if response is not None:
        if response['result'] == "denied":
            deniedMessage()
            display_text.set("")
        elif response['result'] == "otp failed":
            otpFaildMessage()
            display_text.set("")
        else :
            
            window.quit()
            window.destroy()
    else:
        serverMessage()

def add_back(entr, display_text):
    _position = entr.index(INSERT)
    s = display_text.get()
    if(_position != 0):
        s = s[0:_position-1] + s[_position:]
        display_text.set(s)
        entr.icursor(_position-1)
def findPosition(val, entr, display_text):
    _position = entr.index(INSERT)
    s = display_text.get()
    s = s[0:_position] + val + s[_position:]
    display_text.set(s)
    entr.focus_force()
    entr.icursor(_position+1)
    
def goLogin(window):
    global response
    response = {"result":"restart"}
    window.quit()
    window.destroy()
    
def manageEnter(display_text, max):
    val = int(display_text.get())
    print(val)
    if val <= max and val >= 1:
        if manageLocker.sensorState[val]['lockerState'] == 0:
            openMessage(val)
            manageLocker.servoMotorStart(val)
        else:
            alreadyOpen()
    elif val > max:
        valueMessage()
        

class classOTPInput:
    def swap(res):
        
        window = Tk()  
        window.geometry("1280x960")
        window.resizable(False,False)
        
        window['bg'] = backGroundColor
        
        canvas = Canvas(window, relief="solid",height=1, width = 1140, bg = mint, highlightcolor = backGroundColor, highlightbackground = backGroundColor, highlightthickness = 2)
        canvas.grid(row=1,column=0,columnspan=12,sticky="ne")
        canvas.create_line(0,0,100,0,fill="red")
        
        Label(window, text = "프작남",fg=colorBack,bg = backGroundColor,height=2, width=8,font=("basic",20, "bold")).grid(pady=8,row = 0, column = 0,columnspan=2)
        Label(window, text = "공공 사물함 대여 서비스",fg=colorBack,bg = backGroundColor,height=2, width=16,font=("basic",20, "bold")).grid(pady=8,row = 0, column = 0,columnspan=12,sticky="e",ipadx=40)

        ro = 8
        co = 8
        Label(window,fg=backGroundColor,bg = backGroundColor,height=4, width=4).grid(row = 2, column = 0)
        Label(window,fg=backGroundColor,bg = backGroundColor,height=4, width=4).grid(row = 2, column = 11)
        Label(window,fg=backGroundColor,bg = backGroundColor,height=ro, width=co).grid(row = 3, column = 4)
        Label(window,fg=backGroundColor,bg = backGroundColor,height=ro, width=co).grid(row = 4, column = 4)
        Label(window,fg=backGroundColor,bg = backGroundColor,height=ro, width=co).grid(row = 5, column = 4)
        Label(window,fg=backGroundColor,bg = backGroundColor,height=ro, width=co).grid(row = 6, column = 4)
        
        display_text = StringVar()
        # 사용자 id와 password를 저장하는 변수 생성
        entr = Entry(window, font=("basic",30),width = 13,textvariable = display_text,bg="White",highlightthickness=4,highlightcolor= "#5bbfb5", highlightbackground = backGroundColor)
        entr.grid(row = 3, column = 1, columnspan = 4,padx=100,sticky="e")
        entr.focus_force()
        Val = [['1','2','3'],['4','5','6'],['7','8','9']]
        
        Row = [710,900,1090]
        Col = [0,193,386]
        btnsize = 36
        # 0~11 -> KeyPad(10 Back, 11 Enter), 12 처음으로, 13 or ,  14 NFC
        target = [None for i in range(15)]
        keyrow = 3
        keycol = 5
        for j in range(3):
            for i in range(3):
                target[j*3+i] = Button(window, text=Val[j][i],font=("basic",btnsize), height=2, width=5, command=partial(findPosition,Val[j][i], entr, display_text), takefocus = False)
                target[j*3+i].grid(row = keyrow+j, column = keycol+i*2 ,columnspan=2, sticky = "ns")
        
        target[9] = Button(window, text='0',font=("basic",btnsize), height=2, width=5, command=partial(findPosition,'0',entr,display_text), takefocus = False)
        target[9].grid(row = keyrow+3, column = keycol+2 ,columnspan=2, sticky = "ns")
        target[10] = Button(window, text="back",font=("basic",btnsize), height=2, width=5, command=partial(add_back, entr, display_text), takefocus = False)
        target[10].grid(row = keyrow+3, column = keycol+4 ,columnspan=2, sticky = "ns")
        
        target[11] = Button(window, text="Enter",font=("basic",btnsize), height=2, width=5)
        target[11].grid(row = keyrow+3, column = keycol ,columnspan=2, sticky = "ns")
        
        target[12] = Button(window, text="처음으로",font=("basic",btnsize-15,"bold"),height=1, width=7, command=partial(goLogin,window))
        target[12].grid(row = 2, column = 1,rowspan = 2, padx=15,ipady=1, pady = 10, sticky = "n")
        
        #or
        target[13] = Label(window, font=("basic",28), bg="White", fg ="#5CFFD1")
        target[13].grid(row = 4, column = 1,columnspan=4,sticky = "s")
        #nfc
        target[14] = Label(window, font=("basic",28), bg="White", fg ="#5CFFD1")
        target[14].grid(row = 5, column = 1,rowspan=2,columnspan=4,sticky = "n")
        
        for i in range(13):
            target[i]["bg"] = backGroundColor
            target[i]["fg"] = keyColorBtnText
            target[i]["activebackground"] = keyColorBtnActiveBack
            target[i]["activeforeground"] = keyColorBtnActiveText
            target[i]["highlightthickness"] = 2
            target[i]["highlightbackground"] = colorBack
            target[i]["relief"] = "flat"
        target[12]["fg"] = "Red"

        for i in range(13,15):
            target[i]["bg"] = backGroundColor
            target[i]["fg"] = keyColorBtnText
            target[i]["highlightthickness"] = 2
            target[i]["highlightbackground"] = backGroundColor

        if res == 0:
            target[13]["text"] = "OTP를"
            target[14]["text"] = "입력해주세요"
            target[11]["command"] = partial(add_Enter,window,display_text)
        else:
            target[13]["text"] = "개폐할 사물함의"
            target[14]["text"] = "번호를 입력하세요"
            target[11]["command"] = partial(manageEnter, display_text, res)
        
        window.mainloop()