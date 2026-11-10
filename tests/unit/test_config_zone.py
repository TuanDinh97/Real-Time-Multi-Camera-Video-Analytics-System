import pytest
from pydantic import ValidationError

from occ.common.config import CameraConfig, ZoneConfig

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]


def minimal_zone(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "zone-1",
        "space_id": "room-01",
        "group": "room",
        "kind": "room",
        "capacity": 6,
        "assign": "overlap",
        "polygon": SQUARE,
    }
    data.update(overrides)
    return data


def test_valid_zone_uses_spec_defaults() -> None:
    zone = ZoneConfig.model_validate(minimal_zone())
    assert zone.anchor_y == 0.5
    assert zone.overlap_min == 0.3
    assert zone.polygon[2] == (100, 100)


@pytest.mark.parametrize(
    ("polygon", "reason"),
    [
        ([[0, 0], [100, 0]], "at least 3 points"),
        ([[0, 0], [100, 100], [100, 0], [0, 100]], "Self-intersection"),
        ([[0, 0], [50, 50], [100, 100]], "Self-intersection"),
        ([[-1, 0], [100, 0], [100, 100]], "greater than or equal to 0"),
    ],
)
def test_bad_polygon_is_rejected(polygon: list[list[int]], reason: str) -> None:
    with pytest.raises(ValidationError, match=reason):
        ZoneConfig.model_validate(minimal_zone(polygon=polygon))


def test_duplicate_zone_ids_in_one_camera_are_rejected() -> None:
    camera = {
        "schema_version": 1,
        "camera_id": "cam-1",
        "source": "rtsp://mediamtx:8554/cam-1",
        "zones": [minimal_zone(), minimal_zone()],
    }
    with pytest.raises(ValidationError, match="duplicate zone id"):
        CameraConfig.model_validate(camera)
