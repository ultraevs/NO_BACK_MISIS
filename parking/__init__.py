from ultralytics import YOLO
import parking.detection


def current_model(file):
    model = YOLO(file)
    return model
