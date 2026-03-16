def test_prices_requires_auth(client):
    response = client.get("/api/v1/products/1/prices")
    assert response.status_code == 401


def test_add_price_success(client, auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={"price": 39.90}
    )
    data = response.get_json()

    assert response.status_code == 201
    assert {"id", "product_id", "price", "collected_at"}.issubset(data)
    assert data["product_id"] == product_obj.id
    assert data["price"] == 39.90


def test_add_price_missing_data(client, auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={}
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "Missing data" in data["error"]


def test_add_price_missing_price_field(client, auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={"anything": 10}
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "Price is required" in data["error"]


def test_add_price_invalid_price_type(client, auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={"price": "invalid"}
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "Price must be a number" in data["error"]


def test_add_price_invalid_price_value(client, auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={"price": 0}
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "Price must be greater than 0" in data["error"]


def test_add_price_product_not_found(client, auth_header):
    response = client.post(
        "/api/v1/products/999/prices",
        headers=auth_header,
        json={"price": 39.90}
    )
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]


def test_add_price_from_another_user_product(client, second_auth_header, product):
    product_obj, _ = product

    response = client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=second_auth_header,
        json={"price": 39.90}
    )
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]


def test_view_product_prices_success(client, auth_header, product):
    product_obj, _ = product

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header
    )
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert {"id", "product_id", "price", "collected_at"}.issubset(data[0])


def test_view_product_prices_sorted_desc(client, auth_header, product):
    product_obj, _ = product

    client.post(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header,
        json={"price": 39.90}
    )

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=auth_header
    )
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["collected_at"] >= data[1]["collected_at"]


def test_view_product_prices_product_not_found(client, auth_header):
    response = client.get("/api/v1/products/999/prices", headers=auth_header)
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]


def test_view_product_prices_from_another_user_product(client, second_auth_header, product):
    product_obj, _ = product

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices",
        headers=second_auth_header
    )
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]


def test_view_product_prices_stats_success(client, auth_header, product_with_multiple_prices):
    product_obj, _ = product_with_multiple_prices

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices/stats",
        headers=auth_header
    )
    data = response.get_json()

    assert response.status_code == 200
    assert {
        "current",
        "average",
        "lowest",
        "highest",
        "total",
        "variation_percent",
        "is_best_price",
        "last_30_days_average",
        "price_trend",
    }.issubset(data)

    assert data["current"] == 110.0
    assert data["average"] == 100.0
    assert data["lowest"] == 90.0
    assert data["highest"] == 110.0
    assert data["total"] == 3
    assert data["variation_percent"] == 10.0
    assert data["is_best_price"] is False
    assert data["last_30_days_average"] == 100.0
    assert data["price_trend"] == "up"


def test_view_product_prices_stats_with_fields_filter(client, auth_header, product_with_multiple_prices):
    product_obj, _ = product_with_multiple_prices

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices/stats?fields=current,lowest,price_trend",
        headers=auth_header
    )
    data = response.get_json()

    assert response.status_code == 200
    assert set(data.keys()) == {"current", "lowest", "price_trend"}
    assert data["current"] == 110.0
    assert data["lowest"] == 90.0
    assert data["price_trend"] == "up"


def test_view_product_prices_stats_invalid_fields(client, auth_header, product):
    product_obj, _ = product

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices/stats?fields=current,banana",
        headers=auth_header
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "Invalid stats fields: banana" in data["error"]


def test_view_product_prices_stats_product_not_found(client, auth_header):
    response = client.get("/api/v1/products/999/prices/stats", headers=auth_header)
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]


def test_view_product_prices_stats_from_another_user_product(client, second_auth_header, product):
    product_obj, _ = product

    response = client.get(
        f"/api/v1/products/{product_obj.id}/prices/stats",
        headers=second_auth_header
    )
    data = response.get_json()

    assert response.status_code == 404
    assert "product not found" in data["error"]