from httpx import AsyncClient

PAYLOAD = {"email": "engineer@dgp.ru", "name": "Инженер", "password": "secret123"}


async def test_create_user_returns_server_generated_fields(client: AsyncClient) -> None:
    """created_at приходит от БД: без RETURNING его дочитывание после commit упало бы."""
    response = await client.post("/api/users", json=PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == PAYLOAD["email"]
    assert body["created_at"]
    assert "password" not in body
    assert "hashed_password" not in body


async def test_create_user_rejects_duplicate_email(client: AsyncClient) -> None:
    await client.post("/api/users", json=PAYLOAD)

    response = await client.post("/api/users", json={**PAYLOAD, "name": "Другой"})

    assert response.status_code == 409


async def test_list_users_returns_created(client: AsyncClient) -> None:
    await client.post("/api/users", json=PAYLOAD)

    response = await client.get("/api/users")

    assert response.status_code == 200
    assert [user["email"] for user in response.json()] == [PAYLOAD["email"]]
