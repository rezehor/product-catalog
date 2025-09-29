import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_filter(client: AsyncClient, filter_one_template):
    """
    Test creating a new filter with valid conditions.
    """

    response = await client.post("/filters/", json=filter_one_template)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    res_data = response.json()
    assert res_data["name"] == "Filter1", "Filter name mismatch."
    assert len(res_data["conditions"]) == 2, "Expected one condition in the filter."
    assert res_data["logical_operator"] == "OR", "Logical operator mismatch."


@pytest.mark.asyncio
async def test_create_duplicate_filter(client: AsyncClient, filter_one_template):
    """
    Test creating a filter with a duplicate name.
    """

    await client.post("/filters/", json=filter_one_template)
    response = await client.post("/filters/", json=filter_one_template)

    assert response.status_code == 409, f"Expected 409, got {response.status_code}"


@pytest.mark.asyncio
async def test_get_all_filters(
    client: AsyncClient, filter_one_template, filter_two_template
):
    """
    Test retrieving all filters.
    """
    await client.post("/filters/", json=filter_one_template)
    await client.post("/filters/", json=filter_two_template)

    response = await client.get("/filters/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    filters = response.json()
    assert len(filters) >= 2, "Expected at least 2 filters in the list."

    names = [f["name"] for f in filters]
    assert "Filter1" in names, "Filter1 not found in response."
    assert "Filter2" in names, "Filter2 Two not found in response."


@pytest.mark.asyncio
async def test_get_filter_by_name(client: AsyncClient, filter_one_template):
    """
    Test retrieving a filter by its name.
    """
    await client.post("/filters/", json=filter_one_template)

    response = await client.get("/filters/Filter1/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    filter_ = response.json()
    assert filter_["name"] == "Filter1", "Filter name mismatch."


@pytest.mark.asyncio
async def test_update_filter(client: AsyncClient, filter_one_template):
    """
    Test updating an existing filter.
    """
    await client.post("/filters/", json=filter_one_template)

    update_data = {
        "conditions": [
            {
                "logical_operator": "OR",
                "conditions": [
                    {"field": "test1", "operator": "<", "value": 50},
                    {"field": "test2", "operator": "<=", "value": 100},
                ],
            },
            {
                "logical_operator": "OR",
                "conditions": [
                    {"field": "test3", "operator": "regex", "value": "3"},
                    {"field": "test4", "operator": ">=", "value": 200},
                ],
            },
        ],
    }
    response = await client.patch("/filters/Filter1/", json=update_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert (
        data["conditions"][0]["conditions"][0]["operator"] == "<"
    ), "Condition operator mismatch."
    assert (
        data["conditions"][0]["conditions"][0]["value"] == 50
    ), "Value was not updated."
    assert (
        data["conditions"][0]["conditions"][1]["operator"] == "<="
    ), "Condition operator mismatch."
    assert (
        data["conditions"][1]["conditions"][0]["operator"] == "regex"
    ), "Condition operator mismatch."
    assert (
        data["conditions"][1]["logical_operator"] == "OR"
    ), "Logical operator was not updated."


@pytest.mark.asyncio
async def test_delete_filter(client: AsyncClient, filter_one_template):
    """
    Test deleting a filter by name.
    """
    await client.post("/filters/", json=filter_one_template)

    response = await client.delete("/filters/Filter1/")
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"

    response = await client.get("/filters/Filter1/")
    assert response.status_code == 404, "Deleted filter should not be retrievable."


@pytest.mark.asyncio
async def test_filter_validation_empty_conditions(client: AsyncClient):
    """
    Test creating a filter with empty conditions (should fail validation).
    """
    data = {
        "name": "Filter1",
        "logical_operator": "OR",
        "conditions": [],
    }

    response = await client.post("/filters/", json=data)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


@pytest.mark.asyncio
async def test_create_filter_with_default_operator(client: AsyncClient):
    """
    Test creating a filter without explicitly setting logical_operator
    (should default to AND).
    """
    data = {
        "name": "Filter",
        "conditions": [
            {
                "conditions": [
                    {"field": "test1", "operator": ">", "value": 100},
                ]
            }
        ],
    }

    response = await client.post("/filters/", json=data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    res_data = response.json()
    assert res_data["name"] == "Filter", "Filter name mismatch."
    assert (
        res_data["logical_operator"] == "AND"
    ), f"Expected default logical_operator 'AND', got {res_data['logical_operator']}"
    assert (
        res_data["conditions"][0]["conditions"][0]["field"] == "test1"
    ), "Field mismatch."
