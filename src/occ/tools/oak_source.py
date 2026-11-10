import time
from types import TracebackType
from typing import Self

import depthai as dai
import numpy as np
import numpy.typing as npt


class OAKVideoSource:
    def __init__(self, width: int = 640, height: int = 400, fps: int = 20) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline: dai.Pipeline | None = None
        self.queue: dai.MessageQueue | None = None

    def __enter__(self) -> Self:
        self.pipeline = dai.Pipeline()
        camera = self.pipeline.create(dai.node.Camera).build()
        self.queue = camera.requestOutput(
            (self.width, self.height), fps=self.fps
        ).createOutputQueue()
        self.pipeline.start()
        return self

    def read(self) -> tuple[npt.NDArray[np.uint8], int]:
        if self.queue is None:
            raise RuntimeError("OAKVideoSource must be used inside a 'with' block")
        packet = self.queue.get()
        if not isinstance(packet, dai.ImgFrame):
            raise TypeError(f"Expected ImgFrame, got {type(packet).__name__}")
        frame = packet.getCvFrame()
        timestamp_ns = time.monotonic_ns()
        return frame, timestamp_ns

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.pipeline is not None:
            self.pipeline.stop()
