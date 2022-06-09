from tkinter import Toplevel, Label
from componentColor import backGroundColorEx, colorBack
def reset(win):
    win.destroy()
class MessageWindow(Toplevel):
    def __init__(self, message):
        super().__init__()
        a = self
        a.geometry("520x140+400+290")
        a["highlightthickness"] = 3
        a["highlightbackground"] = backGroundColorEx
        colorBack = "#5bbfb5"
        a["bg"] = colorBack 
        a.resizable(False, False)
        a.rowconfigure(0, weight=0)
        a.rowconfigure(1, weight=1)
        a.columnconfigure(0, weight=1)
        a.columnconfigure(1, weight=1)
        a.overrideredirect(True)
        Label(self, text=message,font = ("basic",20, "bold"),bg = colorBack, fg = "White").place(relx = 0.5, rely = 0.5, anchor = 'center')
        a.after(3000, reset,a)
    pass

def otpFaildMessage():
    MessageWindow("다시 한번 입력해 주세요(OTP 값 오류)")
def deniedMessage():
    MessageWindow("다시 한번 입력해 주세요(사물함 오류)")
    
def idpwMessage():
    MessageWindow("ID or PW를 다시 입력해주세요")
def overdueMessage():
    MessageWindow("연체되었습니다. 관리자에게 문의하세요")
def serverMessage():
    MessageWindow("서버 점검 중. 관리자에게 문의하세요")
def valueMessage():
    MessageWindow("존재하지 않는 사물함입니다.")
def openMessage(index):
    MessageWindow(str(index) + "번 사물함이 열렸습니다.")
def alreadyOpen():
    MessageWindow("이미 열린 사물함입니다.")