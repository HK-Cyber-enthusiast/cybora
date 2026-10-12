from cybora.modules.dependencies import scan


def test_unpinned_dependency(tmp_path):
    target = tmp_path / "requirements.txt"
    target.write_text("requests\nhttpx>=0.28\n", encoding="utf-8")
    findings = scan(str(target))
    assert any(f.title == "Unpinned dependency" for f in findings)
