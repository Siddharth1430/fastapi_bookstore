from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_get_books():
    """
    Tests the get books function.
    This test check that all books is displaued
    """
    response = client.get("/books/all")
    assert response.status_code==200
    assert isinstance(response.json(), list)
    
def test_get_filtred_book():
    """
    Tests the get filtered books function.
    This test checks the books are filterd by either title or author name
    """ 
    response = client.get("/books/")
    assert response.status_code==200
    assert isinstance(response.json(), list)
    
def test_get_individual_book():
    """
    Tests the get individual book function.
    This test check that books is displayed for given bookid
    """
    response = client.get("/books/1")
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}
   
def test_create_book():
    """
    Tests the create book function.
    This test checks whether the book is created with the correct attrubutes
    """
    book= { "id": 101,"title": "aaa","description": "nice book", "edition": 1, "author_id": 1}
    response = client.post("/books", json=book)
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Book already exist"}
        
def test_update_book():
    """
    Tests the update book function.
    This test checks that updation is done for given book id
    """
    book = { "id": 101,"title": "aaa","description": "nice book", "edition": 1, "author_id": 1}
    response = client.put("/books/1",json=book)
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    elif response.status_code == 404:
        assert response.json() == {"detail": "Book already exist"}
    else:
        assert response.status_code == 409
        assert response.json() == {"detail": "Book already exist with same title"}
     
def test_delete_books():
    """
    Tests the delete book function.
    This test checks that given book id is deleted
    """
    response = client.delete("/books/1")
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() =={"detail" :"Item not found"}
        
