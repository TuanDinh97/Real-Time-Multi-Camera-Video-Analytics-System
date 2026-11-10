"""Configuration models (spec: Cấu hình, D6)."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

# Id: chữ thường, số, nối bằng "-". Ví dụ: mkb-oak1, room-01
Id = Annotated[str, Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$", max_length=64)]
RtspUrl = Annotated[str, Field(pattern=r"^rtsp://")]


class StrictModel(BaseModel):
    """Base for config models: unknown keys are errors, objects are read-only."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class DetectorConfig(StrictModel):
    conf: float = Field(default=0.30, ge=0.0, le=1.0)
    min_box_h: int = Field(default=24, ge=0)


class SeatConfig(StrictModel):
    t_in_s: float = Field(default=10, gt=0)
    grace_s: float = Field(default=60, gt=0)
    min_session_s: float = Field(default=30, ge=0)


class FeatureFlag(StrictModel):
    enabled: bool = False


class CameraConfig(StrictModel):
    schema_version: Literal[1]
    camera_id: Id
    source: RtspUrl
    sample_fps: float = Field(default=2, gt=0, le=30)
    detector: DetectorConfig = Field(default_factory=DetectorConfig)
    exclusions: list[dict[str, object]] = Field(default_factory=list)  # 3.3: model riêng
    zones: list[dict[str, object]] = Field(default_factory=list)  # 3.3: model riêng
    seat: SeatConfig = Field(default_factory=SeatConfig)
    tracking: FeatureFlag = Field(default_factory=FeatureFlag)
    door_counter: FeatureFlag = Field(default_factory=FeatureFlag)
