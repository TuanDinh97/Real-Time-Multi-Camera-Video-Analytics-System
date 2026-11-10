# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# if not cap.isOpened():
#     raise RuntimeError("Cannot open camera")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     cv2.imshow("Computer Vision Camera", frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import depthai as dai

with dai.Pipeline() as pipeline:
    cam = pipeline.create(dai.node.Camera).build()
    queue = cam.requestOutput((640, 400)).createOutputQueue()

    pipeline.start()

    while pipeline.isRunning():
        frame = queue.get()
        cv2.imshow("Luxonis OAK Camera", frame.getCvFrame())

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()
