import pytest
from httpx import AsyncClient

SCHEDULE = {
    "stages": [
        {
            "code": "12.3.2",
            "name": "Устройство свай",
            "planned_start": "2024-01-15",
            "planned_end": "2024-03-31",
        },
        {
            "code": "12.4.31",
            "name": "Кровля",
            "planned_start": "2024-08-01",
            "planned_end": "2024-09-30",
            "checkable_by_equipment": False,
        },
    ]
}


async def create_site(client: AsyncClient, code: str = "p08") -> str:
    response = await client.post("/api/sites", json={"code": code, "name": "ЖК на Ленинском"})
    assert response.status_code == 201
    return response.json()["id"]


async def test_site_code_is_unique(client: AsyncClient) -> None:
    await create_site(client)

    response = await client.post("/api/sites", json={"code": "p08", "name": "ещё раз"})

    assert response.status_code == 409


async def test_schedule_import_replaces_previous(client: AsyncClient) -> None:
    site_id = await create_site(client)

    await client.put(f"/api/sites/{site_id}/schedule", json=SCHEDULE)
    response = await client.put(
        f"/api/sites/{site_id}/schedule",
        json={"stages": [{"code": "12.3.1", "name": "Устройство котлована"}]},
    )

    assert response.status_code == 200
    assert [stage["code"] for stage in response.json()] == ["12.3.1"]


async def test_schedule_rejects_duplicate_codes(client: AsyncClient) -> None:
    site_id = await create_site(client)

    response = await client.put(
        f"/api/sites/{site_id}/schedule",
        json={"stages": [{"code": "1.1", "name": "Раз"}, {"code": "1.1", "name": "Два"}]},
    )

    assert response.status_code == 422


async def test_status_round_trip_matches_contract(client: AsyncClient) -> None:
    site_id = await create_site(client)
    await client.put(f"/api/sites/{site_id}/schedule", json=SCHEDULE)

    upsert = {
        "as_of": "2024-04-24",
        "stages": [
            {
                "stage_code": "12.3.2",
                "status": "behind",
                "delay_days": 24,
                "basis": "работы наблюдаются после плановой даты окончания",
                "confidence": "medium",
                "evidence_dates": ["2024-02-21", "2024-04-24"],
            },
            {
                "stage_code": "12.4.31",
                "status": "not_checkable",
                "basis": "этап не определяется по технике",
            },
        ],
    }
    assert (await client.put(f"/api/sites/{site_id}/status", json=upsert)).status_code == 200

    response = await client.get(f"/api/sites/{site_id}/status", params={"as_of": "2024-04-24"})

    assert response.status_code == 200
    body = response.json()
    assert body["site_id"] == "p08"
    piles = next(stage for stage in body["stages"] if stage["stage_code"] == "12.3.2")
    assert piles["status"] == "behind"
    assert piles["delay_days"] == 24
    assert piles["planned"] == {"start": "2024-01-15", "end": "2024-03-31"}
    assert piles["evidence_dates"] == ["2024-02-21", "2024-04-24"]


@pytest.mark.parametrize(
    ("stage_code", "status"),
    [("12.4.31", "behind"), ("12.3.2", "not_checkable")],
)
async def test_status_respects_checkability(
    client: AsyncClient, stage_code: str, status: str
) -> None:
    """CONTRACTS §2: непроверяемый по технике этап не может стать нарушением, и наоборот."""
    site_id = await create_site(client)
    await client.put(f"/api/sites/{site_id}/schedule", json=SCHEDULE)

    response = await client.put(
        f"/api/sites/{site_id}/status",
        json={"as_of": "2024-04-24", "stages": [{"stage_code": stage_code, "status": status}]},
    )

    assert response.status_code == 422


async def test_status_rejects_unknown_stage(client: AsyncClient) -> None:
    site_id = await create_site(client)
    await client.put(f"/api/sites/{site_id}/schedule", json=SCHEDULE)

    response = await client.put(
        f"/api/sites/{site_id}/status",
        json={"as_of": "2024-04-24", "stages": [{"stage_code": "99.9", "status": "behind"}]},
    )

    assert response.status_code == 422


async def test_status_rejects_value_outside_contract(client: AsyncClient) -> None:
    site_id = await create_site(client)
    await client.put(f"/api/sites/{site_id}/schedule", json=SCHEDULE)

    response = await client.put(
        f"/api/sites/{site_id}/status",
        json={"as_of": "2024-04-24", "stages": [{"stage_code": "12.3.2", "status": "ок"}]},
    )

    assert response.status_code == 422
