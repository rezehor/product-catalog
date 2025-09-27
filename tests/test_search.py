import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_products_with_a_filter(
    client: AsyncClient, filter_one_template, products_template
):
    """
    Test searching products with a valid filter that matches results.
    """
    await client.post("/filters/", json=filter_one_template)
    await client.post("/products/", json={"products": products_template})

    response = await client.get("/search/Filter1/?page=1&per_page=10")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert (
        len(data["products"]) == 2
    ), f"Expected 2 products, got {len(data['products'])}"
    assert data["products"][0]["name"] == "Product1", "Expected 'Product1' in response"
    assert data["products"][1]["name"] == "Product2", "Expected 'Product2' in response"


@pytest.mark.asyncio
async def test_search_filter_not_found(client: AsyncClient):
    """
    Test searching with a non-existent filter returns 404.
    """
    response = await client.get("/search/NonExistentFilter/")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    assert "not found" in detail, f"Unexpected error message: {detail}"


@pytest.mark.asyncio
async def test_search_no_products_found(client: AsyncClient, filter_one_template):
    """
    Test searching with a valid filter but no matching products returns 404.
    """

    await client.post("/filters/", json=filter_one_template)

    response = await client.get("/search/Filter1/")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    assert "No products found" in detail, f"Unexpected error message: {detail}"
