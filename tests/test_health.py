def test_health_check(client):
    """Test du endpoint health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
