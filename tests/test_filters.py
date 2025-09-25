import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_filter(client: AsyncClient):
    data = {
        "name": "PriceFilter",
        "conditions": [
            {"field": "price", "operator": ">", "value": 100}
        ],
        "logical_operator": "AND"
    }
    response = await client.post("/filters/", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["name"] == "PriceFilter"
    assert len(res_data["conditions"]) == 1
    assert res_data["logical_operator"] == "AND"


@pytest.mark.asyncio
async def test_create_duplicate_filter(client: AsyncClient):
    data = {
        "name": "DuplicateFilter",
        "conditions": [
            {"field": "price", "operator": ">", "value": 50}
        ]
    }

    await client.post("/filters/", json=data)
    response = await client.post("/filters/", json=data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_all_filters(client: AsyncClient):

    await client.post("/filters/", json={
        "name": "Filter1",
        "conditions": [{"field": "price", "operator": ">", "value": 10}]
    })
    await client.post("/filters/", json={
        "name": "Filter2",
        "conditions": [{"field": "price", "operator": "<", "value": 100}]
    })

    response = await client.get("/filters/")
    assert response.status_code == 200
    filters = response.json()
    assert len(filters) >= 2
    names = [filter_["name"] for filter_ in filters]
    assert "Filter1" in names and "Filter2" in names


@pytest.mark.asyncio
async def test_get_filter_by_name(client: AsyncClient):
    await client.post("/filters/", json={
        "name": "SpecialFilter",
        "conditions": [{"field": "name", "operator": "==", "value": "Phone"}]
    })
    response = await client.get("/filters/SpecialFilter/")
    assert response.status_code == 200
    filter_ = response.json()
    assert filter_["name"] == "SpecialFilter"


@pytest.mark.asyncio
async def test_update_filter(client: AsyncClient):
    await client.post("/filters/", json={
        "name": "UpdateFilter",
        "conditions": [{"field": "price", "operator": ">", "value": 100}]
    })
    update_data = {
        "logical_operator": "OR",
        "conditions": [{"field": "price", "operator": ">=", "value": 150}]
    }
    response = await client.patch("/filters/UpdateFilter/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["logical_operator"] == "OR"
    assert data["conditions"][0]["operator"] == ">="


@pytest.mark.asyncio
async def test_delete_filter(client: AsyncClient):
    await client.post("/filters/", json={
        "name": "DeleteFilter",
        "conditions": [{"field": "price", "operator": ">", "value": 50}]
    })
    response = await client.delete("/filters/DeleteFilter/")
    assert response.status_code == 204

    response = await client.get("/filters/DeleteFilter/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_filter_validation_empty_conditions(client: AsyncClient):
    data = {"name": "InvalidFilter", "conditions": []}
    response = await client.post("/filters/", json=data)
    assert response.status_code == 422
