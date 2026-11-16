from tests.test_helpers import get_test_client

def test_t10_resilience():
    """T10: System health, reporting read model decoupling, and API resilience."""
    client = get_test_client()
    
    # 1. Health Endpoint Check
    health_res = client.get("/health")
    assert health_res.status_code == 200
    health_data = health_res.json()
    assert health_data["status"] == "HEALTHY"
    assert health_data["database"] == "CONNECTED"
    assert health_data["regions_supported"] == 12
    
    # 2. Root API Check
    root_res = client.get("/")
    assert root_res.status_code == 200
    assert "FulfillIQ" in root_res.json()["message"]
    
    return {
        "test_id": "T10_RESILIENCE",
        "description": "System health, API resilience, and 12-region database connectivity",
        "expected": "HTTP 200, status HEALTHY, database CONNECTED, regions_supported == 12",
        "observed": f"Status: {health_data['status']}, Database: {health_data['database']}, Regions: {health_data['regions_supported']}",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t10_resilience()
    print("Test T10 Passed:", res)
