from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_otpgenerator():
    """
    Tests the OTP generation function.
    This test generates only to the registerd phone_number
    """
    otp= { "phone_number" : "9876543210" }
    response = client.post("/generateotp", json=otp)
    if response.status_code== 200:
        assert isinstance(response.json(), str)
        
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "User with this phone numner not exist"}
        
def test_verifier():
    """
    Tests the OTP verification function.
    This test verifies whether opt is valid or not
    """
    otp={"phone_number":"9876543210","otp": "343590"}
    response=client.post("/verify", json= otp)
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 401
        assert response.json() == {"detail":"Invalid Otp"}
    