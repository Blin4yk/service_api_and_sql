from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestIntegration:
    def test_sync_and_list_flow(self):
        # Тестируем полный цикл: синхронизация -> получение данных
        sync_response = client.post("/sync?page=1&limit=10")
        assert sync_response.status_code == 200

        list_response = client.get("/items")
        assert list_response.status_code == 200
        data = list_response.json()
        assert isinstance(data, list)

    def test_external_api(self):
        response = client.get("/external/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        active_items = [item for item in data if not item.get("is_deleted", False)]
        assert len(active_items) >= 1
