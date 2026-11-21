from app.scanners.text_scanner import scan_text

def test_clean_text():
    assert scan_text("hello world").sensitive is False

def test_marker_detected_case_insensitive():
    assert scan_text("prefix WALLED_SENSITIVE suffix").sensitive is True
    assert scan_text("walled_sensitive").sensitive is True
