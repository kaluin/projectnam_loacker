
from tkinter import Tk, Button, Entry, Label, Toplevel, DISABLED, Canvas
from functools import partial
import manageLocker
from componentColor import *
from restApi import send_api
from messageBox import *
locker_sensor =  { 1:{'motor':2,'magnetic':3}, 2:{'motor':4,'magnetic':17},
                   3:{'motor':14,'magnetic':15}, 4:{'motor':18,'magnetic':23}}
response = None
def reset(canUse):
    canUse.quit()
    canUse.destroy()
def reset_all(window1,window2):
    reset(window1)
    reset(window2)
    
def oneday_reserve(canUse):
    senddata={"id":None,"lockername":None,"otp":None}
    response=send_api("/locker/oneday_rent", "POST", senddata)
    if response is not None:
        if response['result'] == "denied":    
            deniedMessage()
        elif response['result'] == "otp failed":
            otpFaildMessage()
        else:          
            Bel = Toplevel(canUse)
            Bel.geometry("1280x960")
            Bel.resizable(False,False)
            Bel['bg'] = backGroundColor
            
            canvas = Canvas(Bel, relief="solid",height=1, width = 1140, bg = colorBack, highlightcolor = backGroundColor, highlightbackground = backGroundColor, highlightthickness = 2)
            canvas.place(x = 60, y = 85)
            canvas.create_line(0,0,100,0,fill="red")
            
            laP = Label(Bel, text = "프작남",fg=colorBack,bg = backGroundColor,height=2, width=8,font=("basic",20, "bold"))
            laP.place(x = 92, y = 8)
            laG = Label(Bel, text = "공공 사물함 대여 서비스",fg=colorBack,bg = backGroundColor,height=2, width=16,font=("basic",20, "bold"))
            laG.place(x = 850, y = 8)
            
            Label(Bel, font=("basic",40),text = "{0}번 사물함 문이 열렸습니다.".format(response['lockernum']),bg=backGroundColor, fg = colorBack).place(x=310,y=220)   
            a = manageLocker.servoMotorStart(response['lockernum'])
            Button(Bel, text = "처음으로",height=2, width=8,font=("basic",30), command=partial(reset_all,Bel,canUse), takefocus = False,bg = backGroundColor, fg = keyColorBtnText, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText,highlightthickness=4,highlightbackground= colorBack).place(x=500,y=520)
            
            Bel.mainloop()
            
   
def open_locker(window, URL):
    #response = {'lockernum':1}
    global response
    Bel = Toplevel(window)
    Bel.geometry("1280x960")
    Bel.resizable(False,False)
    Bel['bg'] = backGroundColor
    
    canvas = Canvas(Bel, relief="solid",height=1, width = 1140, bg = colorBack, highlightcolor = backGroundColor, highlightbackground = backGroundColor, highlightthickness = 2)
    canvas.place(x = 60, y = 85)
    canvas.create_line(0,0,100,0,fill="red")
    
    laP = Label(Bel, text = "프작남",fg=colorBack,bg = backGroundColor,height=2, width=8,font=("basic",20, "bold"))
    laP.place(x = 92, y = 8)
    laG = Label(Bel, text = "공공 사물함 대여 서비스",fg=colorBack,bg = backGroundColor,height=2, width=16,font=("basic",20, "bold"))
    laG.place(x = 850, y = 8)
    a = manageLocker.servoMotorStart(response['lockernum'])
    if URL == "deactivate":
        Label(Bel, font=("basic",40),text = "{0}번 사물함 물건을 회수해 주세요.".format(response['lockernum']),bg=backGroundColor, fg = colorBack).place(x=240,y=220)
        manageLocker.neverOpenNotClosed(response['lockernum'])
    else:
        Label(Bel, font=("basic",40),text = "{0}번 사물함 문이 열렸습니다.".format(response['lockernum']),bg=backGroundColor, fg = colorBack).place(x=310,y=220)           
    Button(Bel, text = "처음으로",height=2, width=8,font=("basic",30), command=partial(reset_all,Bel,window) ,takefocus = False, bg = backGroundColor, fg = keyColorBtnText, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText, highlightthickness = 2, highlightbackground = colorBack , relief = "flat").place(x=500,y=520)
    
    
    
    Bel.mainloop()  
def get_locker_num(window, URL):
    global response
    senddata={"id":None,"lockername":None,"otp":None}
    response=send_api("/locker/"+URL, "POST", senddata)
    
    if response is not None:
        if response['result'] == "denied":    
            deniedMessage()
        elif response['result'] == "otp failed":
            otpFaildMessage()
        else:          
            open_locker(window, URL)


class classNFCOTP:
    def __init__(self,ress):
        global response
        response = ress
        
        self.canUse = Tk()
        self.canUse.geometry("1280x960")
        self.canUse.resizable(False,False)        
        
        #self.backGroundColor = "White"
        self.canUse['bg'] = backGroundColor

        
        canvas = Canvas(self.canUse, relief="solid",height=1, width = 1140, bg = colorBack, highlightcolor = backGroundColor, highlightbackground = backGroundColor, highlightthickness = 2)
        canvas.grid(row=1,column=0,columnspan=5,sticky="n")
        canvas.create_line(0,0,100,0,fill="red")
        
        laP = Label(self.canUse, text = "프작남",fg=colorBack,bg = backGroundColor,height=2, width=8,font=("basic",20, "bold"))
        laP.grid(pady=8,row = 0, column = 0,columnspan=1)
        laG = Label(self.canUse, text = "공공 사물함 대여 서비스",fg=colorBack,bg = backGroundColor,height=2, width=16,font=("basic",20, "bold"))
        laG.grid(pady=8,row = 0, column = 3,columnspan=2, ipadx=60)
    def btnSet(self,he,wi,tx,fontSize,com,bgg,fgg,abg,afg,hlt,hlb,re, ro, co):
        bt = Button(self.canUse, text = tx,height=he, width=wi,font=("basic",fontSize),
                    command=com, takefocus = False, bg = bgg, fg = fgg,
                    activebackground = abg, activeforeground = afg,
                    highlightthickness = hlt, highlightbackground = hlb , relief = re)
        bt.grid(row = ro, column = co)
        return bt
    
    def nonReserved(self, maxspaces, usedspaces):
        
        la = [None for i in range(4)]
        bt = [None for i in range(2)]
        designL = [None for i in range(2)]
        
        
        startLabelRow = 3
        startLabelCol = 1
        startBtnRow = startLabelRow + 3
        startBtnCol = startLabelCol
        
        designL[0] = Label(self.canUse,height=5, width = 30, bg=backGroundColor)
        designL[0].grid(row=startLabelRow-1,column=startLabelCol-1)
        designL[1] = Label(self.canUse,height=7, width = 30, bg=backGroundColor)
        designL[1].grid(row=startLabelRow+2,column=startLabelCol+3)
        
        la[0] = Label(self.canUse, font=("basic",40),text = "사용중인 사물함 : ",bg=backGroundColor, fg = keyColorBtnText)
        la[0].grid(row=startLabelRow,column=startLabelCol,sticky = "e")
        la[1] = Label(self.canUse, font=("basic",40),text = "사용가능한 사물함 : ",bg=backGroundColor, fg = keyColorBtnText)
        la[1].grid(row=startLabelRow+1,column=startLabelCol,sticky = "e", ipady=30)
        
        la[2] = Label(self.canUse, font=("basic",40),text = str(usedspaces),bg=backGroundColor, fg = keyColorBtnText)
        la[2].grid(row=startLabelRow,column=startLabelCol+2)
        la[3] = Label(self.canUse, font=("basic",40),text = str(maxspaces-usedspaces),bg=backGroundColor, fg = keyColorBtnText)
        la[3].grid(row=startLabelRow+1,column=startLabelCol+2)
        
        bt[0] = Button(self.canUse, text = "대여하기",height=2, width=8,font=("basic",30) , command=partial(oneday_reserve,self.canUse), takefocus = False)      
        bt[0].grid(row=startBtnRow, column = startBtnCol,sticky = "W")
        bt[1] = Button(self.canUse, text = "처음으로",height=2, width=8,font=("basic",30), command=partial(reset,self.canUse) ,takefocus = False)
        bt[1].grid(row=startBtnRow,column=startBtnCol+2)
        
        for i in range(4):
            la[i]["bg"] = backGroundColor
            la[i]["fg"] = keyColorBtnText
        for i in range(2):
            bt[i]["bg"] = backGroundColor
            bt[i]["fg"] = keyColorBtnText
            bt[i]["activebackground"] = keyColorBtnActiveBack
            bt[i]["activeforeground"] = keyColorBtnActiveText
            bt[i]["highlightthickness"] = 2
            bt[i]["highlightbackground"] = mint
            bt[i]["relief"] = "flat"
        
        if maxspaces==usedspaces:
            bt[0]['state'] = DISABLED
            
        self.canUse.mainloop()
    def reserved(self,isable):
        designL = [None for i in range(2)]
        
        startLabelRow = 3
        startLabelCol = 1
        startBtnRow = startLabelRow + 3
        startBtnCol = startLabelCol
        
        w = 36
        designL[0] = Label(self.canUse,height=5, width = w, bg=backGroundColor)
        designL[0].grid(row=startLabelRow-1,column=startLabelCol-1)
        
        #designL[1] = Label(self.canUse,height=7, width = 30, bg=backGroundColor)
        designL[1] = Label(self.canUse,height=13, width = w, bg=backGroundColor)
        designL[1].grid(row=startLabelRow+1,column=startLabelCol+3)
        
        te = Label(self.canUse, font=("basic",40),text = "  예약된 시간이 아닙니다.",bg=backGroundColor, fg = keyColorBtnText)
        te.grid(row = 3, column =1, columnspan = 3)
        
        if isable == "false":
            b = Button(self.canUse, text = "처음으로",height=2, width=8,font=("basic",32), command=partial(reset,self.canUse), takefocus = False, bg = backGroundColor, fg = keyColorBtnText, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText, highlightthickness = 2, highlightbackground = colorBack , relief = "flat")
            b.grid(row = 5, column = 1, columnspan=3)
        else :
            
            te["text"] = "사용 시작하시겠습니까?"
            designL[0]["width"] = 32
            designL[1]["width"] = 32
            designL[0]["height"] = 7
            Label(self.canUse,height=1, width = 21, bg=backGroundColor).grid(row = 4, column = 2)
            
            star = self.btnSet(2,8,"시작하기",30, partial(get_locker_num,self.canUse, "activate"),backGroundColor,keyColorBtnText, keyColorBtnActiveBack, keyColorBtnActiveText,  2, colorBack, "flat",5,1)
            fi = self.btnSet(2,8," 처음으로", 30, partial(reset,self.canUse),backGroundColor,keyColorBtnText, keyColorBtnActiveBack, keyColorBtnActiveText,  2, colorBack, "flat",5,3)
            
        self.canUse.mainloop()         
    def used(self):
        designL = [None for i in range(2)]
        
        startLabelRow = 3
        startLabelCol = 1
        startBtnRow = startLabelRow + 3
        startBtnCol = startLabelCol
        
        w = 30
        designL[0] = Label(self.canUse,height=5, width = w-4, bg=backGroundColor)
        designL[0].grid(row=startLabelRow-1,column=startLabelCol-1)
        
        designL[1] = Label(self.canUse,height=13, width = w, bg=backGroundColor)
        designL[1].grid(row=startLabelRow+1,column=startLabelCol+3)
        
        Label(self.canUse, font=("basic",40),text = "사물함을 사용중입니다.",bg=backGroundColor, fg = colorBack).grid(row = 3 , column = 1, columnspan = 3 )
        addd = self.btnSet(2,8,"추가 보관",30, partial(open_locker,self.canUse,"justopen"),backGroundColor,keyColorBtnText, keyColorBtnActiveBack, keyColorBtnActiveText,  2, colorBack, "flat",5,1)
        addd.grid(padx=4)
        finn = self.btnSet(2,8,"사용 종료",30, partial(get_locker_num,self.canUse,"deactivate"),backGroundColor,keyColorBtnText, keyColorBtnActiveBack, keyColorBtnActiveText,  2, colorBack, "flat",5,2)
        finn.grid(padx=10)
        staa = self.btnSet(2,8,"처음으로",30, partial(reset,self.canUse),backGroundColor,keyColorBtnText, keyColorBtnActiveBack, keyColorBtnActiveText,  2, colorBack, "flat",5,3)
        staa.grid(padx=10)
        
        self.canUse.mainloop()
    def overdue(self):
        designL = [None for i in range(2)]
        
        startLabelRow = 3
        startLabelCol = 1
        startBtnRow = startLabelRow + 3
        startBtnCol = startLabelCol
        
        w = 39
        designL[0] = Label(self.canUse,height=5, width = w, bg=backGroundColor)
        designL[0].grid(row=startLabelRow-1,column=startLabelCol-1)
        
        designL[1] = Label(self.canUse,height=13, width = w, bg=backGroundColor)
        designL[1].grid(row=startLabelRow+1,column=startLabelCol+3)
        
        
        te = Label(self.canUse, font=("basic",40),text = "연체되었습니다.",bg=backGroundColor, fg = keyColorBtnText)
        te.grid(row = 3, column =1, columnspan = 3)

        te = Label(self.canUse, font=("basic",40),text = "관리자에게 문의하세요",bg=backGroundColor, fg = keyColorBtnText)
        te.grid(row = 4, column =1, columnspan = 3, sticky = "n", ipady=20)

        b = Button(self.canUse, text = "처음으로",height=2, width=8,font=("basic",32), command=partial(reset,self.canUse), takefocus = False, bg = backGroundColor, fg = keyColorBtnText, activebackground = keyColorBtnActiveBack, activeforeground = keyColorBtnActiveText, highlightthickness = 2, highlightbackground = colorBack , relief = "flat")
        b.grid(row = 5, column = 1, columnspan=3)
        
        self.canUse.mainloop()
    pass
