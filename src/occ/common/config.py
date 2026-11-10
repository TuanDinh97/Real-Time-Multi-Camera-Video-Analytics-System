"""Configuration models (spec: Cấu hình, D6)."""

from typing import Annotated, Literal, Self

import shapely
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator
from shapely.validation import explain_validity

# Id: chữ thường, số, nối bằng "-". Ví dụ: mkb-oak1, room-01
Id = Annotated[str, Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$", max_length=64)]
RtspUrl = Annotated[str, Field(pattern=r"^rtsp://")]

# Một điểm trên ảnh, tính bằng pixel: [x, y]
Pixel = Annotated[float, Field(ge=0)]
Point = tuple[Pixel, Pixel]


def _check_polygon(points: list[Point]) -> list[Point]:
    """Reject polygons with < 3 points, zero area or self-intersections."""
    if len(points) < 3:
        raise ValueError(f"polygon needs at least 3 points, got {len(points)}")
    shape = shapely.Polygon(points)
    if not shape.is_valid:
        raise ValueError(f"invalid polygon: {explain_validity(shape)}")
    return points


Polygon = Annotated[list[Point], AfterValidator(_check_polygon)]


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


class ExclusionConfig(StrictModel):
    id: Id
    polygon: Polygon


class ZoneConfig(StrictModel):
    id: Id
    space_id: Id
    group: Id
    kind: Literal["seat", "area", "room"]
    capacity: int = Field(ge=1)
    assign: Literal["point", "overlap"]
    anchor_y: float = Field(default=0.5, ge=0.0, le=1.0)
    overlap_min: float = Field(default=0.3, gt=0.0, le=1.0)
    polygon: Polygon


class CameraConfig(StrictModel):
    schema_version: Literal[1]
    camera_id: Id
    source: RtspUrl
    sample_fps: float = Field(default=2, gt=0, le=30)
    detector: DetectorConfig = Field(default_factory=DetectorConfig)
    exclusions: list[ExclusionConfig] = Field(default_factory=list)
    zones: list[ZoneConfig] = Field(default_factory=list)
    seat: SeatConfig = Field(default_factory=SeatConfig)
    tracking: FeatureFlag = Field(default_factory=FeatureFlag)
    door_counter: FeatureFlag = Field(default_factory=FeatureFlag)

    @model_validator(mode="after")
    def _ids_are_unique(self) -> Self:
        zone_ids = [z.id for z in self.zones]
        duplicates = sorted({i for i in zone_ids if zone_ids.count(i) > 1})
        if duplicates:
            raise ValueError(f"duplicate zone id(s): {', '.join(duplicates)}")
        return self
