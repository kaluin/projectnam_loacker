import requests
import json
from manageOTP import calculate_otp_locker
lockerName = None
name = None
def getName(getName, kind):
    if kind == "lockername":
        global lockerName
        lockerName = getName
    elif kind == "name":
        global name
        name = getName
def send_api(path, method, body):
    if "otp" in body:
        otp, now=calculate_otp_locker()
        body["otp"] = otp
        body["currtime"] = now
    if "id" in body:
        body["id"] = name
    if "lockername" in body:
        body["lockername"] = lockerName
    API_HOST = "http://*.*.*.*:*"
    url = API_HOST + path
    headers = {'charset': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*'}
    
    try:
     if method == 'GET':
        response = requests.get(url, headers=headers)
        return None
     elif method == 'POST':
        data=json.dumps(body, ensure_ascii=False, indent="\t")
        response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t").encode("UTF-8"))
        responsejson=response.json()
        return responsejson
    except Exception as ex:
        print(f"restApi Error")
        return None




