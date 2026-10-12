from cybora.modules.repo import scan


def test_repo_detects_private_key_marker(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("-----BEGIN " + "PRIVATE KEY-----\n", encoding="utf-8")
    findings = scan(str(tmp_path))
    assert any("Private key" in f.title for f in findings)
