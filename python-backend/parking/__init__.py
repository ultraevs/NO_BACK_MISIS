from ultralytics import YOLO

def current_model(file):
    model = YOLO(file)
    return model
