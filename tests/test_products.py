import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, products_template):
    """
    Test the `/products/` endpoint for successfully creating a new product.
    """
    response = await client.post("/products/", json={"products": products_template})
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), f"Expected list response, got {type(data)}"
    assert data[0]["name"] == "Product1", f"Expected 'Product1', got {data[0]['name']}"
    assert data[1]["price"] == 50, f"Expected price 100, got {data[0]['price']}"
    assert data[2]["test3"] == [
        "value"
    ], f"Expected list ['value'], got {data[2]['test']}"


@pytest.mark.asyncio
async def test_create_duplicate_product(client: AsyncClient, products_template):
    """
    Test the `/products/` endpoint for preventing duplicate product names.
    """
    await client.post("/products/", json={"products": products_template})
    response = await client.post("/products/", json={"products": products_template})

    assert response.status_code == 409, f"Expected 409, got {response.status_code}"
    assert (
        response.json()["detail"]
        == "Product with the name ['Product1', 'Product2', 'Product3'] already exists."
    ), (
        f"Expected 'Product with the name ['Product1', 'Product2', 'Product3'] "
        f"already exists.' message, got {response.json()['detail']}"
    )


@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient, products_template):
    """
    Test the `/products/` endpoint for retrieving all products with pagination.
    """
    await client.post("/products/", json={"products": products_template})
    response = await client.get("/products/?page=1&per_page=10")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "products" in data, "Response missing 'products' field."
    assert isinstance(
        data["products"], list
    ), f"Expected list, got {type(data['products'])}"
    assert any(
        product["name"] == "Product2" for product in data["products"]
    ), "Expected 'Product2' in response list."


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, products_template):
    """
    Test the `/products/{product_id}/` endpoint for retrieving a product by ID.
    """
    create_res = await client.post("/products/", json={"products": products_template})
    product_id = create_res.json()[0]["id"]

    response = await client.get(f"/products/{product_id}/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["name"] == "Product1", f"Expected 'Product1', got {data['name']}"
    assert data["price"] == 100, f"Expected price 100, got {data['price']}"


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, products_template):
    """
    Test the `/products/{product_id}/` endpoint for updating a product's details.
    """
    create_res = await client.post("/products/", json={"products": products_template})
    product_id = create_res.json()[0]["id"]

    response = await client.patch(
        f"/products/{product_id}/", json={"price": 200, "test1": 500}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["price"] == 200, f"Expected price 200, got {data['price']}"
    assert data["test1"] == 500, f"Expected price 500, got {data['test1']}"


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, products_template):
    """
    Test the `/products/{product_id}/` endpoint for deleting a product.
    """
    create_res = await client.post("/products/", json={"products": products_template})
    product_id = create_res.json()[0]["id"]

    delete_res = await client.delete(f"/products/{product_id}/")
    assert delete_res.status_code == 204, f"Expected 204, got {delete_res.status_code}"

    get_res = await client.get(f"/products/{product_id}/")
    assert (
        get_res.status_code == 404
    ), f"Expected 404 after delete, got {get_res.status_code}"


@pytest.mark.asyncio
async def test_create_product_invalid_data(client: AsyncClient):
    """
    Test the `/products/` endpoint for rejecting invalid product data.
    """
    response = await client.post(
        "/products/", json={"products": [{"name": "", "price": 100}]}
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    response = await client.post(
        "/products/", json={"products": [{"name": "InvalidProduct", "price": -10}]}
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


@pytest.mark.asyncio
async def test_update_product_wrong_type(client: AsyncClient, products_template):
    """
    Test the `/products/{product_id}/` endpoint for rejecting invalid field types.
    """
    create_res = await client.post(
        "/products/",
        json={"products": products_template},
    )
    product_id = create_res.json()[0]["id"]

    response = await client.patch(f"/products/{product_id}/", json={"test3": 100.00})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.asyncio
async def test_create_products_with_duplicate_names_in_request(client: AsyncClient):
    """
    Test the `/products/` endpoint for rejecting duplicate product names in the same request.
    """
    response = await client.post(
        "/products/",
        json={
            "products": [
                {"name": "FitTrack PRO", "price": 49.99},
                {"name": "FitTrack PRO", "price": 149.00},
            ]
        },
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
