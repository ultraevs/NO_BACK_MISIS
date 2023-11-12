from detection import parking_info
from ultralytics import YOLO

model = YOLO('modelv2.pt')


status = parking_info(model, 2)

print(status)