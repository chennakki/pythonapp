from app.main import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_serves_html():
    res = client().get("/")
    assert res.status_code == 200
    assert b"Multi-Stage Docker Demo" in res.data


def test_health():
    res = client().get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_info_has_version():
    res = client().get("/api/info")
    assert res.status_code == 200
    assert "version" in res.get_json()


def test_static_css():
    res = client().get("/static/style.css")
    assert res.status_code == 200
