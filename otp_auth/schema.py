from pydantic import BaseModel

class OTPGenerator(BaseModel):
    """_summary_
    For generate otp
    Args:
        BaseModel (_type_): _description_
    """
    phone_number : str
    
class Verifier(BaseModel):
    """_summary_
    for verifying the otp
    Args:
        BaseModel (_type_): _description_
    """
    phone_number : str
    otp : str
    

