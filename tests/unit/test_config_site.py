from datetime import date

import pytest
from pydantic import ValidationError

from occ.common.config import SiteConfig


def minimal_site(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "schema_version": 1,
        "site": {"id": "site-1", "name": "Test site", "timezone": "Europe/Moscow"},
        "spaces": [{"id": "room-01", "name": "Room 1", "capacity": 6}],
        "opening_hours": {"mon-fri": ["07:30-21:00"], "sun": []},
        "engine": {"model": "/models/yolo11n.onnx"},
    }
    data.update(overrides)
    return data


def test_minimal_site_uses_spec_defaults() -> None:
    site = SiteConfig.model_validate(minimal_site(holidays=["2027-01-01"]))
    assert site.engine.backend == "ort-cuda"
    assert site.engine.imgsz == 640
    assert site.retention.occupancy_1m_days == 400
    assert site.privacy.debug_save_frames is False
    assert site.holidays == [date(2027, 1, 1)]


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        (
            {"site": {"id": "site-1", "name": "x", "timezone": "Europe/Moskow"}},
            "unknown timezone",
        ),
        (
            {"spaces": [{"id": "a", "name": "A", "capacity": 1}] * 2},
            "duplicate space id",
        ),
        ({"opening_hours": {"mon-fri": ["7:30-21:00"]}}, "should match pattern"),
        ({"opening_hours": {"mon-fri": ["21:00-07:30"]}}, "start must be before end"),
        ({"opening_hours": {"weekdays": ["07:30-21:00"]}}, "should match pattern"),
        ({"engine": {"model": "m.onnx", "imgsz": 650}}, "multiple of 32"),
        ({"engine": {"model": "m.onnx", "backend": "cuda"}}, "ort-cuda"),
    ],
)
def test_invalid_site_is_rejected(overrides: dict[str, object], reason: str) -> None:
    with pytest.raises(ValidationError, match=reason):
        SiteConfig.model_validate(minimal_site(**overrides))
