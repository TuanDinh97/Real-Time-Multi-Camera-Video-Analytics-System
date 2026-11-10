
import time
import cv2
import depthai as dai
import torch
from ultralytics import YOLO
from mcva.sources.oak_source import OAKVideoSource

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("Inference device:", device)

model = YOLO("yolo11n.pt")
model.to(device)

with OAKVideoSource() as source:
    previous = time.perf_counter()

    while True:
        frame, timestamp_ns = source.read()

        start = time.perf_counter()
        result = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=0.35,
            imgsz=640,
            verbose=False
        )[0]

        inference_ms = (time.perf_counter() - start) * 1000
        annotated = result.plot()

        now = time.perf_counter()
        fps = 1.0 / max(now - previous, 1e-6)
        previous = now

        cv2.putText(
            annotated,
            f"FPS: {fps:.1f} | Track: {inference_ms:.1f} ms",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2
        )

        cv2.imshow("OAK - YOLO + ByteTrack", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
