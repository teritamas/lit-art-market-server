import json
from fastapi.testclient import TestClient
from app.master.dataset.models.entry_dataset import (
    EntryDatasetResponse,
)
from app.main import app
from app.master.dataset.models.purchase_dataset import (
    PurchaseDatasetRequest,
    PurchasedDatasetResponse,
)

client = TestClient(app)


def test_entry_dataset_endpoint(mocker):
    # generate_id_strで固定の値を返すmockを作成
    test_dataset_id = "12345"
    mocker.patch(
        "app.master.dataset.services.entry_dataset_service.generate_id_str",
        return_value=test_dataset_id,
    )

    request_payload = {"user_id": "sample data", "description": "sample name"}

    # Make a request to the endpoint with the sample payload
    response = client.post(
        "/dataset",
        files={
            "request": (
                None,
                json.dumps(request_payload),
            ),
            "file": open("./tests/assets/sample_1.jpeg", "rb"),
        },
    )

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["dataset_id"] is not None

    response_model = EntryDatasetResponse(**response_data)
    assert response_model.dataset_id == response_data["dataset_id"]


def test_list_dataset():
    test_entry_dataset_endpoint()

    # Make a request to the endpoint with the sample payload
    response = client.get("/dataset")

    # then
    assert response.status_code == 200
    datasets = response.json()["datasets"]
    assert isinstance(datasets, list)
    assert len(datasets) >= 1


def test_purchase_dataset(mocker):
    test_entry_dataset_endpoint(mocker)

    test_dataset_id = "12345"
    request = PurchaseDatasetRequest(
        user_id="sample_user_id",
    )

    # Send a POST request to the API endpoint
    response = client.post(f"/dataset/{test_dataset_id}/purchased", data=request.json())

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert response.json()["dataset_id"] == test_dataset_id