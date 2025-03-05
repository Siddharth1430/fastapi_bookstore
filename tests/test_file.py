from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_upload_file():
    """
    Tests the file upload function.
    This test cecks the file typr and size
    """
    path ="E:/CERTIFICATE/example1.pdf"
    with open(path,'rb') as f :
        file = {"file": ("example1.pdf", f, "application/pdf")} 
        response = client.post('/files',files=file)
    assert response.status_code == 200
    assert isinstance(response.json(),dict)