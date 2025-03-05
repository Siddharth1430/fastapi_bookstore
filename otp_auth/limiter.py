from fastapi import HTTPException
import time
   
rate_limits = {} 

def rate_limiter(phone_number: str):
    """_summary_
    To check and validate the rate of otp request per user.
    Args:
        phone_number (str): To get the user credential for checking its limit
    Raises:
        HTTPException: If OTP request limit exceeded.
    """
    now = time.time()
    window = 60 
    limit = 2 
    if phone_number not in rate_limits:
        rate_limits[phone_number] = []
    previous_requests = rate_limits[phone_number]
    valid_requests = []
    for t in previous_requests:
        if now - t < window:
            valid_requests.append(t)  
    rate_limits[phone_number] = valid_requests    

    if len(rate_limits[phone_number]) >= limit:
        raise HTTPException(status_code=429, detail="OTP request limit exceeded. Try again later.")
    rate_limits[phone_number].append(now)
    
    
    
