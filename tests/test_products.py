import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    response = await client.post(
        "/products/",
        json={"products": [{"name": "Laptop", "price": 1500.50}]}
    )
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Laptop"
    assert data[0]["price"] == 1500.50
    assert "id" in data[0]


@pytest.mark.asyncio
async def test_create_duplicate_product(client: AsyncClient):
    await client.post(
        "/products/", json={"products": [{"name": "Phone", "price": 999.99}]}
    )
    response = await client.post(
        "/products/", json={"products": [{"name": "Phone", "price": 888.88}]}
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient):
    await client.post(
        "/products/", json={"products": [{"name": "TestProduct", "price": 123.45}]}
    )

    response = await client.get("/products/?page=1&per_page=10")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert any(p["name"] == "TestProduct" for p in data["products"])


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    create_res = await client.post(
        "/products/", json={"products": [{"name": "Mouse", "price": 49.99}]}
    )
    product_id = create_res.json()[0]["id"]

    response = await client.get(f"/products/{product_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mouse"
    assert data["price"] == 49.99


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    create_res = await client.post(
        "/products/", json={"products": [{"name": "Keyboard", "price": 120.00}]}
    )
    product_id = create_res.json()[0]["id"]

    response = await client.patch(
        f"/products/{product_id}/", json={"price": 100.00}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 100.00


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    create_res = await client.post(
        "/products/", json={"products": [{"name": "Monitor", "price": 300.00}]}
    )
    product_id = create_res.json()[0]["id"]

    delete_res = await client.delete(f"/products/{product_id}/")
    assert delete_res.status_code == 204

    get_res = await client.get(f"/products/{product_id}/")
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_create_product_invalid_data(client: AsyncClient):
    response = await client.post(
        "/products/", json={"products": [{"name": "", "price": 100}]}
    )
    assert response.status_code == 422

    response = await client.post(
        "/products/", json={"products": [{"name": "InvalidProduct", "price": -10}]}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_product_wrong_type(client: AsyncClient):
    create_res = await client.post(
        "/products/",
        json={"products": [{"name": "Keyboard", "price": 120.00, "is_light": True}]}
    )
    product_id = create_res.json()[0]["id"]

    response = await client.patch(
        f"/products/{product_id}/", json={"is_light": 100.00}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_products_with_duplicate_names_in_request(client: AsyncClient):
    response = await client.post(
        "/products/",
        json={
            "products": [
                {"name": "FitTrack PRO", "price": 49.99},
                {"name": "FitTrack PRO", "price": 149.00}
            ]
        }
    )
    assert response.status_code == 422
