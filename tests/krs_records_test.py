def test_hello(client):
    response = client.get("/krs/")
    assert response.status_code == 200 and response.get_data(as_text=True) == "Hello GLH"
