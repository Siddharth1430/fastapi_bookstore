from otp_auth.schema import Verifier,OTPGenerator
from models import Users
from fastapi import HTTPException
import hashlib
import os
from utils import create_access_token,create_refresh_token
import secrets
from datetime import timedelta
import time
from otp_auth.limiter import rate_limiter
secret = secrets.token_hex(32)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

class OTPAuthentication():
    def __init__(self,session):
        """
        Constructor for OTPAuthentication class.
        """
        self.session = session
        
    def generate_otp(self,user : OTPGenerator):
        """_summary_
        To generate a new OTP for user
        Args:
            user (GenerateOTP): it has phone number
        Raises:
            HTTPException:If User with this phone numner not exist.
        Returns:
            str : otp 
        """
        print(user.phone_number)
        rate_limiter(user.phone_number) 
        results = self.session.query(Users).filter(Users.phone_number== user.phone_number).first()
        if not results :
            raise HTTPException(status_code=404, detail="User with this phone numner not exist")   
        otp_dict={}
        uptime = os.times().elapsed 
        time_interval =int(uptime // 60)
        data = f"{user.phone_number}{secret}{time_interval}".encode()
        hash_value = hashlib.sha256(data).hexdigest()
        otp = hash_value[:6] 
        otp_dict[user.phone_number] = {"otp": otp,"expiry": time.time() + 1800}
        return otp   
    
    def verify_via_phone_number(self,user : Verifier):
        """_summary_
        Verifing the otp with credential like ph num
        Args:
            user (VerifyByPhoneNumber): it has both ph num ans otp.
        Raises:
            HTTPException:If Invalid Otp.
        Returns:
            str of access and refresh tokens
        """
        otp = self.generate_otp(user)
        if otp != user.otp:
            raise HTTPException(status_code=401, detail="Invalid Otp")
        access_token = create_access_token({"sub": user.otp}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token({"sub": user.otp},timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        return {"access_token": access_token, "refresh_token": refresh_token}
    





    
