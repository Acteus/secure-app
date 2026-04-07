from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        JSONIFY_PRETTYPRINT_REGULAR=False,
        MAX_CONTENT_LENGTH=32 * 1024,  # 32KB request cap
    )

    @app.after_request
    def set_security_headers(resp):  # type: ignore[no-untyped-def]
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["Content-Security-Policy"] = "default-src 'none'"
        return resp

    @app.get("/healthz")
    def healthz():  # type: ignore[no-untyped-def]
        return jsonify(status="ok"), 200

    @app.post("/v1/echo")
    def echo():  # type: ignore[no-untyped-def]
        if request.mimetype != "application/json":
            return jsonify(error="content_type_must_be_application_json"), 415

        data: Any = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="invalid_json_object"), 400

        msg = data.get("message")
        if not isinstance(msg, str):
            return jsonify(error="message_must_be_string"), 400

        msg = msg.strip()
        if not (1 <= len(msg) <= 200):
            return jsonify(error="message_length_out_of_range"), 400

        return jsonify(message=msg), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "8080")),
        debug=False,
    )

