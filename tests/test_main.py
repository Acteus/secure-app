from app.main import create_app


def test_healthz_ok():
    app = create_app()
    client = app.test_client()

    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_echo_requires_json_content_type():
    app = create_app()
    client = app.test_client()

    resp = client.post("/v1/echo", data="not-json", headers={"Content-Type": "text/plain"})
    assert resp.status_code == 415
    assert resp.get_json()["error"] == "content_type_must_be_application_json"


def test_echo_validates_body_shape_and_message_rules():
    app = create_app()
    client = app.test_client()

    resp = client.post("/v1/echo", json=["nope"])
    assert resp.status_code == 400

    resp = client.post("/v1/echo", json={"message": 123})
    assert resp.status_code == 400

    resp = client.post("/v1/echo", json={"message": ""})
    assert resp.status_code == 400

    resp = client.post("/v1/echo", json={"message": "  hello  "})
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "hello"}


def test_security_headers_present():
    app = create_app()
    client = app.test_client()

    resp = client.get("/healthz")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "no-referrer"
    assert "default-src 'none'" in resp.headers["Content-Security-Policy"]

