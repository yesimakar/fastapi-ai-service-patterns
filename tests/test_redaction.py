from app.utils.redaction import redact_mapping


def test_redacts_sensitive_keys():
    result = redact_mapping({"api_key": "abc", "nested": {"token": "secret"}, "safe": "ok"})

    assert result["api_key"] == "[redacted]"
    assert result["nested"]["token"] == "[redacted]"
    assert result["safe"] == "ok"
