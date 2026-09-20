from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.models import Visit

def visit(client, section, session_id=None):
    return client.post(
        "/visits", json={"section": section, "session_id": str(session_id or uuid4())}
    )


def test_stats_start_at_zero(client):
    res = client.get("/visits/stats")

    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 0
    assert {s["section"] for s in body["sections"]} == {
        "about",
        "portfolio",
        "skills",
        "experience",
    }


def test_counts_and_sorts_by_visits(client):
    visit(client, "portfolio")
    visit(client, "portfolio")
    visit(client, "skills")

    body = client.get("/visits/stats").json()

    assert body["total"] == 3
    assert body["sections"][0] == {"section": "portfolio", "visits": 2}
    assert body["sections"][1] == {"section": "skills", "visits": 1}


def test_same_session_counts_once(client):
    session_id = uuid4()

    assert visit(client, "about", session_id).status_code == 204
    assert visit(client, "about", session_id).status_code == 204

    assert client.get("/visits/stats").json()["total"] == 1


def test_rejects_unknown_section(client):
    assert visit(client, "admin").status_code == 422


def test_days_filter_ignores_older_visits(client, db):
    visit(client, "about")
    db.add(Visit(section="skills", session_id=str(uuid4()), created_at=datetime.now(timezone.utc) - timedelta(days=30)))
    db.commit()

    all_time = client.get("/visits/stats").json()
    last_week = client.get("/visits/stats", params={"days": 7}).json()

    assert all_time["total"] == 2
    assert last_week["total"] == 1
    assert last_week["days"] == 7


def test_days_must_be_a_real_window(client):
    assert client.get("/visits/stats", params={"days": 0}).status_code == 422


def test_stats_are_cacheable(client):
    res = client.get("/visits/stats")

    assert res.headers["cache-control"] == "public, max-age=30"