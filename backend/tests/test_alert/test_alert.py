import pytest
from src.alert import determine_alert_level
from src.detection.grade_signal import SignalResult

def test_determine_alert_level_stable():
    assert determine_alert_level(0, False) == "stable"

def test_determine_alert_level_watch():
    assert determine_alert_level(1, False) == "watch"

def test_determine_alert_level_review():
    assert determine_alert_level(2, False) == "review"
    assert determine_alert_level(3, False) == "review"

def test_determine_alert_level_suppressed():
    # 2 signals usually means review, but seasonal suppressed -> watch
    assert determine_alert_level(2, True) == "watch"

def test_determine_alert_level_improving():
    # Previous was review, currently 0 signals -> improving
    assert determine_alert_level(0, False, "review") == "improving"
    assert determine_alert_level(0, False, "watch") == "improving"
    assert determine_alert_level(0, False, "stable") == "stable"
