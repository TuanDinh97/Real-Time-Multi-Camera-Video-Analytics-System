import pytest
from pydantic import ValidationError

from occ.common.config import CameraConfig


def minimal_camera(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "schema_version": 1,
        "camera_id": "cam-1",
        "source": "rtsp://mediamtx:8554/cam-1",
    }
    data.update(overrides)
    return data


def test_minimal_camera_uses_spec_defaults() -> None:
    cam = CameraConfig.model_validate(minimal_camera())
    assert cam.sample_fps == 2
    assert cam.detector.conf == 0.30
    assert cam.tracking.enabled is False


def test_unknown_field_is_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        CameraConfig.model_validate(minimal_camera(smaple_fps=2))


@pytest.mark.parametrize(
    "overrides",
    [
        {"camera_id": "cam_1"},  # id có dấu "_"
        {"schema_version": 2},  # phiên bản lạ
        {"detector": {"conf": 1.5}},  # conf > 1
        {"source": "http://mediamtx/cam-1"},  # không phải rtsp://
        {"sample_fps": 0},  # phải > 0
    ],
)
def test_invalid_camera_is_rejected(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CameraConfig.model_validate(minimal_camera(**overrides))
