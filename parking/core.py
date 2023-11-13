from detection import parking_info
from ultralytics import YOLO

model = YOLO('modelv2.pt')


answer = parking_info(model, 1)
print(answer)