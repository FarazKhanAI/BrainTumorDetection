from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # base YOLOv8 nano
model.train(
    data="dataset.yaml",
    epochs=20,
    imgsz=640,
    batch=16,
    device="cpu",
    name="brain_tumor_detection"
)
