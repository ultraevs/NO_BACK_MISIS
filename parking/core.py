from detection import parking_info
from ultralytics import YOLO

model = YOLO('model.pt')


parking_info(model, 1)