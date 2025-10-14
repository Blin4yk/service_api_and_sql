from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestItemAPI:
    def test_list_items(self):
        response = client.get("/items")
        assert response.status_code == 200

    def test_sync_items(self):
        response = client.post("/sync?page=1&limit=10")
        assert response.status_code == 200
        assert "synced" in response.json()

    def test_external_api(self):
        response = client.get("/external/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
