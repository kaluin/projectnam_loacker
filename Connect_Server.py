from restApi import send_api, getName
from dbm import post, set
info = post()
getName(info[0], "lockername")
if info[4]!=0: # first connection
    senddata={"lockername":info[0], "location":info[1], "maxspaces":info[2]}
    while True:
        response = send_api("/locker/connect", "POST", senddata)
        if response is not None:
            if response['result']=="success":
                set("otpkey", response['otpkey'])
                set("isNeverConnected",0)
                break
            else:
                print("이건 서버에서 이상한 값이 넘어온건데")
        else:
            print("서버 꺼져있음")

else:        # not first connection
    senddata={"lockername":None,"otp":None}
    while True:
        response = send_api("/locker/connect", "POST", senddata)
        if response is not None:
            if response['result'] == "success":
                print('connected to server.')
                break
            else:
                print("이건 서버에서 이상한 값이 넘어온건데")
        else:
            print("Connect_Error : 서버 꺼져있음")
