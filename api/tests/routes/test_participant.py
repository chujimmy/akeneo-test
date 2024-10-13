class TestParticipantRoutes:
    def test_get_participants_returns_200(self, client):
        response = client.get("/participants/")

        assert response.status_code == 200
        assert response.json == {"participants": ["foo", "bar"]}
