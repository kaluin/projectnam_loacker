from pyotp import TOTP
from hashlib import sha256
from base64 import b32encode
from datetime import datetime
import dbm

def calculate_otp_locker():
    info = dbm.post()
    key=str(dbm.get("otpkey"))
    totp=TOTP(b32encode(bytes(key, 'utf-8')), 6, sha256)
    now=str(datetime.now())
    result=totp.at(datetime.strptime(now, '%Y-%m-%d %H:%M:%S.%f'))
    return result, now

def calculate_otp(key):
    totp=TOTP(b32encode(bytes(key, 'utf-8')), 6, sha256)
    now=str(datetime.now())

    result=totp.at(datetime.strptime(now, '%Y-%m-%d %H:%M:%S.%f'))
    return result, now