from fastapi.testclient import TestClient
from main import app
from fastapi import HTTPException

client = TestClient(app)

def test_get_books():
    response = client.get("/books/all")
    assert response.status_code==200
    assert isinstance(response.json(), list)
    
def test_get_individual_book():
    response = client.get("/books/1")
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}
        
def test_get_author():
    response = client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    
def test_create_book():
    book= { "id": 101,"title": "aaa","description": "nice book", "edition": 1, "author_id": 1}
    response = client.post("/books", json=book)
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Book already exist"}

def test_upload_file():
    path ="E:/CERTIFICATE/example1.pdf"
    with open(path,'rb') as f :
        file = {"file": ("example1.pdf", f, "application/pdf")} 
        response = client.post('/files',files=file)
    assert response.status_code == 200
    assert isinstance(response.json(),dict)
    
def test_create_author():
    author={"author_id" : 101,"name":"kanishka","no_of_books_published": 10}
    response = client.post("/books/101/author",json=author)
    assert response.status_code==200
    assert isinstance(response.json(),dict)
    
def test_update_book():
    book = { "id": 101,"title": "aaa","description": "nice book", "edition": 1, "author_id": 1}
    response = client.put("/books/1",json=book)
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    elif response.status_code == 404:
        assert response.json() == {"detail": "Book already exist"}
    else:
        assert response.status_code == 409
        assert response.json() == {"detail": "Book already exist with same title"}

def test_update_author():
    author={"author_id" : 101,"name":"kanishka","no_of_books_published": 10}
    response = client.put("/authors/1",json=author)  
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() =={"detail" :"Author not found"}
     
def test_delete_books():
    response = client.delete("/books/1")
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() =={"detail" :"Item not found"}
        
def test_delete_author():
    response = client.delete("/authors/1")
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    elif response.status_code == 404:
        assert response.json() =={"detail" :"Author not found"}
    else:
        assert response.status_code == 409
        assert response.json() =={"detail" :"Cannot delete author having books"}