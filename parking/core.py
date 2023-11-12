from detection import parking_info
from ultralytics import YOLO

model = YOLO('modelv2.pt')


parking_info(model, 0)