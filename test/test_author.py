from fastapi.testclient import TestClient
from main import app

client = TestClient(app)       

def test_get_author():
    """
    Tests the get authirs function.
    This test check that all author is displaued
    """
    response = client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    
def test_create_author():
    """
    Tests the create author function.
    This test checks whether the author is created with the correct attrubutes
    """
    author={"author_id" : 101,"name":"kanishka","no_of_books_published": 10}
    response = client.post("/books/101/author",json=author)
    assert response.status_code==200
    assert isinstance(response.json(),dict)
    
def test_update_author():
    """
    Tests the update author function.
    This test checks that updation is done for given author id
    """
    author={"author_id" : 101,"name":"kanishka","no_of_books_published": 10}
    response = client.put("/authors/1",json=author)  
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    else:
        assert response.status_code == 404
        assert response.json() =={"detail" :"Author not found"}
        
def test_delete_author():
    """
    Tests the delete author function.
    This test checks that given author id is deleted
    """
    response = client.delete("/authors/1")
    if response.status_code == 200:
        assert isinstance(response.json(),dict)
    elif response.status_code == 404:
        assert response.json() =={"detail" :"Author not found"}
    else:
        assert response.status_code == 409
        assert response.json() =={"detail" :"Cannot delete author having books"}