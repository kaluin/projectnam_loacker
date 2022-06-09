from time import sleep


import NFCOTP
import ClassLoginFinish
from messageBox import MessageWindow, serverMessage
import canUsed
from Connect_Server import info
maxLockerNum = info[2]

while True:
    try:
        login = ClassLoginFinish
        login.classLogin().login()
        
        if login.response is not None:
            if login.response['result'] == "success":
                result = None
                NFCOTP.classOTPInput.swap(0)
                locker = NFCOTP.response
                result = locker['result']
                if result is not None:
                    if result != 'restart':
                        if result == "admin":
                            NFCOTP.classOTPInput.swap(maxLockerNum)
                        else:
                            asa = canUsed.classNFCOTP(locker)
                            if result == "idle" :
                                asa.nonReserved(locker['maxspaces'], locker['usedspaces'])
                            elif result == "reserved":
                                asa.reserved(locker['isable'])
                            elif result == "using":
                                asa.used()
                            elif result == "overdue":
                                asa.overdue()
                            else:
                                serverMessage()
                                pass
                            del asa
                    elif result != "restart":
                        serverMessage()
                del locker
        del login
    except Exception as e:
        print("error")
        serverMessage()
        sleep(3)


