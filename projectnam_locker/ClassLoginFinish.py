from tkinter import Tk,StringVar,Label,Entry,Button,INSERT,Canvas
from functools import partial
from restApi import send_api, getName
from messageBox import *
from componentColor import *
                    
focusedLabel = 0
# 0 : ID 1 : password
_display_text = [None, None]
_entr = [None, None]

def findPosition(val):
    _position = _entr[focusedLabel%2].index(INSERT)
    s = _display_text[focusedLabel%2].get()
    s = s[0:_position] + val + s[_position:]
    _display_text[focusedLabel%2].set(s)
    _entr[focusedLabel%2].focus_force()
    _entr[focusedLabel%2].icursor(_position+1)

def focuschanged():
    global focusedLabel
    focusedLabel+=1
    _entr[focusedLabel%2].focus_force()

def callfocuschanged(e):
    focuschanged()
    
def password_btn(PASSWD):
    global focusedLabel
    focusedLabel=1

def user_id_btn(ID):
    global focusedLabel
    focusedLabel=2

# 사용자 id와 password를 비교하는 함수
def check_data(_window):
    global response
    inputID=_display_text[0].get()
    inputPW=_display_text[1].get()
    
    getName(inputID, "name")
    senddata={"lockername":None,"otp":None, "id":inputID, "pw":inputPW}
    
    response=send_api("/locker/login", "POST", senddata)
    if response is not None: 
        if response['result'] == "success" :
            print("logged in successfully")
            
            _display_text[0] = None
            _display_text[1] = None
            
            
            _window.quit()
            _window.destroy()
        elif response['result'] == "denine":
            deniedMessage()
        elif response['result'] == "otp error":
            deniedMessage()
        elif response['result'] == "id pw error":
            idpwMessage()
    else:
        serverMessage()
    

def add_s(value):
    findPosition(value) 
    
def clear_all():
    _display_text[0].set('')
    _display_text[1].set('')

def add_Enter():
    findPosition('')

def add_back():   
    _position = _entr[focusedLabel%2].index(INSERT)
    s = _display_text[focusedLabel%2].get()
    if(_position != 0):
        s = s[0:_position-1] + s[_position:]
        _display_text[focusedLabel%2].set(s)
        _entr[focusedLabel%2].icursor(_position-1)

class classLogin:
    def login(self):
        global _display_text, _entr, response
        _window = Tk()
        _window.title(' 사물함 대여 서비스(프작남) ')
        _window.geometry("1280x960")
        _window.resizable(False,False)
        _window.lift()
        _window['bg'] = backGroundColor
        
        # 0 : ID 1 : password
        _display_text = [ StringVar(), StringVar()]
        _entr = ['','']
        response = None
        
        textStartRow = 0
        textStartLabelRow = textStartRow+2
        textBtnStartRow = textStartLabelRow+3
        
        canvas = Canvas(_window, relief="solid",height=1, width = 1110, bg = mint, highlightcolor = backGroundColor, highlightbackground = backGroundColor, highlightthickness = 2)
        canvas.grid(row=1,column=0,columnspan=10,sticky="n")
        canvas.create_line(0,0,100,0,fill="red")
        
        Label(_window, text = "프작남",fg=colorBack,bg = backGroundColor,height=2, width=8,font=("basic",20, "bold")).grid(pady=8,row = 0+textStartRow, column = 0,columnspan=2)
        Label(_window, text = "공공 사물함 대여 서비스",fg=colorBack,bg = backGroundColor,height=2, width=16,font=("basic",20, "bold")).grid(pady=8,row = 0+textStartRow, column = 0,columnspan=10,sticky="e",ipadx=80)
               
        Label(_window, font=("basic",15, "bold"),text = "Username : ",fg= colorBack, bg = backGroundColor).grid(row = textStartLabelRow, column = 1 ,columnspan=2)
        Label(_window, font=("basic",15, "bold"),text = "Password : ",fg= colorBack, bg = backGroundColor).grid(row = textStartLabelRow+1, column = 1 ,columnspan=2)
        
        _entr[0] = Entry(_window, font=("basic",15),textvariable = _display_text[0],bg="White",highlightthickness=4,highlightcolor= "#5bbfb5", highlightbackground = backGroundColor)
        _entr[0].grid(row = textStartLabelRow, column = 2, padx=70,pady=20,ipady=15, columnspan=4, sticky = "w")
        _entr[0].bind('<Button-1>',user_id_btn)
        _entr[0].focus_force()

        _entr[1] = Entry(_window, font=("basic",15),textvariable = _display_text[1], show='*',bg="White",highlightthickness=4,highlightcolor= "#5bbfb5", highlightbackground = backGroundColor)
        _entr[1].grid(row = textStartLabelRow+1, column = 2 , padx=70,pady=5,ipady=15,columnspan=4, sticky = "w")
        _entr[1].bind('<Button-1>',password_btn)
        
        Button(_window, text = "Login",fg=colorText,bg = colorBack, activebackground = colorActiveBack, activeforeground = colorActiveText,relief = "flat",height=2, width=8,font=("basic",20), command = partial(check_data,_window), takefocus = False,highlightthickness=2,highlightbackground= backGroundColor).grid(row = textStartLabelRow, column = 6,rowspan=2, columnspan = 2)
        
        Label(_window,fg=colorBack,bg = backGroundColor,height=1, width=4).grid(row = textStartLabelRow+2, column = 0)
        
        Val = [['!','@','#','$','%','^','&','*','(',')'], ['1','2','3','4','5','6','7','8','9','0'], ['q','w','e','r','t','y','u','i','o','p'],
         ['a','s','d','f','g','h','j','k','l','space'], ['z','x','c','v','b','n','m','next','back',None]]
        HEIGHT = [1,2,2,2,2]
        btnsize = 29
        for i in range(0,10):
            Button(_window, relief = "flat", text=Val[0][i],bg = keyColorBtnBack, fg = keyColorBtnText, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText,font=("basic",btnsize), height=HEIGHT[0], width=4, highlightthickness=1,highlightbackground= "#5bbfb5",command=partial(findPosition,Val[0][i]), takefocus = False).grid(row=textBtnStartRow, column=i)
        for j in range(1,4):
            for i in range(0,10):
                Button(_window, relief = "flat", text=Val[j][i],bg = backGroundColor, fg = colorBack, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText,highlightthickness=1,highlightbackground= "#5bbfb5",font=("basic",btnsize), height=HEIGHT[j], width=4, command=partial(findPosition,Val[j][i]), takefocus = False).grid(row=j+textBtnStartRow, column=i)
        for i in range(0,7):
            Button(_window, relief = "flat", text=Val[4][i],bg = backGroundColor, fg = colorBack, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText,highlightthickness=1,highlightbackground= "#5bbfb5",font=("basic",btnsize), height=HEIGHT[4], width=4, command=partial(findPosition,Val[4][i]), takefocus = False).grid(row=4+textBtnStartRow, column=i, columnspan=2)                    

        Clear = Button(_window,relief = "flat", bg = backGroundColor, fg = "#ff0000", activebackground = "#AA0000",activeforeground = "#ffffff",text="Clear",font=("basic",btnsize-3,"bold"), height=2, width=4, command=clear_all, takefocus = False, highlightthickness=1,highlightbackground= "#5bbfb5")
        Clear.grid(row=3+textBtnStartRow, column=9, sticky = "nsew")
        Back = Button(_window, relief = "flat",text="back",font=("basic",btnsize-3, "bold"), height=2, width=4, command=add_back, takefocus = False,bg = backGroundColor, fg = "#ff0000", activebackground = "#AA0000",activeforeground = "#ffffff", highlightthickness=1,highlightbackground= "#5bbfb5")
        Back.grid(row=4+textBtnStartRow, column=8, sticky = "ns", columnspan=2)
        Next = Button(_window, relief = "flat",text="next",font=("basic",btnsize, "bold"), height=2, width=4, command=focuschanged, takefocus = False,bg = backGroundColor, fg = "Blue", activebackground = "Blue",activeforeground = "#ffffff", highlightthickness=1,highlightbackground= "#5bbfb5")
        Next.grid(row=4+textBtnStartRow, column=7, sticky = "ns", columnspan=2)
        
        _window.mainloop()
    pass
