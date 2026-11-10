
import time
import depthai as dai


class OAKVideoSource:
    def __init__(self, width=640, height=400, fps=20):
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline = None
        self.queue = None

    def __enter__(self):
        self.pipeline = dai.Pipeline()

        camera = self.pipeline.create(
            dai.node.Camera
        ).build()

        self.queue = camera.requestOutput(
            (self.width, self.height),
            fps=self.fps
        ).createOutputQueue()

        self.pipeline.start()
        return self

    def read(self):
        packet = self.queue.get()
        frame = packet.getCvFrame()
        timestamp_ns = time.monotonic_ns()
        return frame, timestamp_ns

    def __exit__(self, exc_type, exc_value, traceback):
        if self.pipeline is not None:
            self.pipeline.stop()
